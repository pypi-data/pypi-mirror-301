import logging
from typing import Any, Callable, Final

import numpy as np

from pyrfx.config_manager import ConfigManager
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.utils import determine_swap_route, get_available_tokens


class OrderArgumentParser:
    """
    A parser to handle and process order arguments for increase, decrease, or swap operations on the RFX Exchange.

    This class processes user-supplied order parameters, ensures all required parameters are present,
    fills in missing parameters where possible, and raises exceptions for critical missing data.

    :param config: Configuration object containing network details.
    :param operation_type: The type of operation ('increase', 'decrease', or 'swap').
    """

    def __init__(self, config: ConfigManager, operation_type: str) -> None:
        """
        Initializes the LiquidityArgumentParser class with the necessary configuration and operation type.

        :param config: Configuration object containing chain and market settings.
        :param operation_type: Specifies the type of operation ('increase', 'decrease', or 'swap').
        :raises ValueError: If an unknown operation type is provided.
        :return: None
        """
        self.config: ConfigManager = config
        self.parameters: dict = {}
        self.operation_type: str = operation_type
        self._allowed_operation_types: Final[list[str]] = ["increase", "decrease", "swap"]
        if operation_type not in self._allowed_operation_types:
            error_message: str = (
                f'Operation type {operation_type} is not valid. Valid types: {", ".join(self._allowed_operation_types)}'
            )
            logging.error(error_message)
            raise ValueError(error_message)

        # Set required keys based on operation type
        self.required_keys: list[str] = self._set_required_keys()

        self._available_markets: dict[str, dict[str, Any]] | None = None

        self.missing_base_key_methods: dict[str, Callable[[], None]] = {
            "index_token_address": self._handle_missing_index_token_address,
            "market_key": self._handle_missing_market_key,
            "start_token_address": self._handle_missing_start_token_address,
            "out_token_address": self._handle_missing_out_token_address,
            "collateral_address": self._handle_missing_collateral_address,
            "swap_path": self._handle_missing_swap_path,
            "is_long": self._handle_missing_is_long,
            "slippage_percent": self._handle_missing_slippage_percent,
            "initial_collateral_delta": self._handle_missing_initial_collateral_delta,
        }

    def process_parameters(self, parameters: dict) -> dict[str, Any]:
        """
        Processes the input dictionary and fills in missing keys if possible. Raises exceptions if
        critical data is missing.

        The method:
        - Identifies missing keys in the supplied parameters.
        - Fills in missing data like `swap_path`, `collateral_address`, etc.
        - Validates parameters, including position size and maximum leverage limits for non-swap operations.

        :param parameters: Dictionary containing order parameters.
        :return: Processed dictionary with missing keys filled in.
        """

        missing_keys: list[str] = self._determine_missing_keys(parameters)
        self.parameters: dict[str, Any] = parameters

        for missing_key in missing_keys:
            if missing_key in self.missing_base_key_methods:
                self.missing_base_key_methods[missing_key]()

        if self.operation_type == "swap":
            self.calculate_missing_position_size_info_keys()
            self._check_if_max_leverage_exceeded()

        if self.operation_type == "increase" and self._calculate_initial_collateral_usd() < 2:
            raise Exception("Position size must be backed by >= $2 of collateral!")

        self._format_size_info()
        return self.parameters

    def _set_required_keys(self) -> list[str]:
        """
        Set the list of required keys based on the operation type (increase, decrease, or swap).

        :return: A list of required keys for the specified operation.
        """
        if self.operation_type == "increase":
            return [
                "index_token_address",
                "market_key",
                "start_token_address",
                "collateral_address",
                "swap_path",
                "is_long",
                "size_delta_usd",
                "initial_collateral_delta",
                "slippage_percent",
            ]
        elif self.operation_type == "decrease":
            return [
                "index_token_address",
                "market_key",
                "start_token_address",
                "collateral_address",
                "is_long",
                "size_delta_usd",
                "initial_collateral_delta",
                "slippage_percent",
            ]
        elif self.operation_type == "swap":
            return [
                "start_token_address",
                "out_token_address",
                "initial_collateral_delta",
                "swap_path",
                "slippage_percent",
            ]
        else:
            return []

    def _determine_missing_keys(self, parameters_dict: dict) -> list:
        """
        Compare the supplied dictionary keys with the required keys for creating an order.

        :param parameters_dict: Dictionary of user-supplied parameters.
        :return: A list of missing keys.
        """
        return [key for key in self.required_keys if key not in parameters_dict]

    def _handle_missing_index_token_address(self) -> None:
        """
        Handles missing 'index_token_address'. Attempts to infer the address from the token symbol.
        Raises an exception if neither index token address nor symbol is provided.

        :raises Exception: If neither index token address nor symbol is provided.
        :return: None.
        """
        token_symbol: str | None = self.parameters.get("index_token_symbol")

        if not token_symbol:
            logging.error("'index_token_symbol' does not exist in parameters!")
            raise Exception("'index_token_symbol' does not exist in parameters!")

        # Adjust the token symbol if needed (e.g., for BTC)
        if token_symbol == "BTC":
            token_symbol = "WBTC.b"

        # Retrieve the token address by symbol
        self.parameters["index_token_address"] = self._find_key_by_symbol(
            get_available_tokens(config=self.config), token_symbol
        )

    def _handle_missing_market_key(self) -> None:
        """
        Handles the case where the 'market_key' is missing. Attempts to infer the market key based on the
        provided 'index_token_address'. Handles specific known exceptions for certain token addresses.
        Raises a ValueError if the 'index_token_address' is missing or if no market key can be inferred.

        :raises ValueError: If the 'index_token_address' is missing or cannot infer the market key.
        """
        index_token_address: str | None = self.parameters.get("index_token_address")

        if not index_token_address:
            logging.error("Index Token Address is missing. Cannot infer market key without it.")
            raise ValueError("Index Token Address is missing. Cannot infer market key without it.")

        # Handle specific known exceptions for index token addresses
        token_address_overrides: dict[str, str] = {
            "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f": "0x47904963fc8b2340414262125aF798B9655E58Cd"
        }

        # Apply override if the index token address matches a known exception
        original_address = index_token_address
        index_token_address = token_address_overrides.get(index_token_address, index_token_address)

        if original_address != index_token_address:
            logging.info(f"Index token address {original_address} overridden to {index_token_address}.")

        # Attempt to find the market key from available markets using the index token address
        self.parameters["market_key"] = self._find_market_key_by_index_address(index_token_address)

    def _find_market_key_by_index_address(self, index_token_address: str) -> str:
        """
        Finds the market key for the given index token address.

        :param index_token_address: The address of the index token.
        :return: The market key corresponding to the index token address.
        :raises ValueError: If the index token address is not found.
        """
        if not self._available_markets:
            self._available_markets: dict[str, dict[str, Any]] = Markets(self.config).get_available_markets()

        # Use next() for more efficient searching
        market_key = next(
            (
                key
                for key, market_info in self._available_markets.items()
                if market_info.get("index_token_address") == index_token_address
            ),
            None,
        )

        if market_key:
            logging.info(f"Market key found: {market_key} for index token address: {index_token_address}")
            return market_key

        logging.error(f"Market key not found for index token address: {index_token_address}")
        raise ValueError(f"Market key not found for index token address: {index_token_address}")

    def _handle_missing_token_address(
        self, token_type: str, symbol_key: str, address_key: str, known_symbols: dict[str, str] | None = None
    ) -> None:
        """
        General handler for missing token addresses. Infers the address from the token symbol.

        :param token_type: A string describing the type of token (e.g., 'start', 'out', 'collateral').
        :param symbol_key: The key for the token symbol in the parameters.
        :param address_key: The key for the token address to be inferred and stored in the parameters.
        :param known_symbols: Optional dictionary of known symbols with pre-defined addresses.
        :raises ValueError: If the token symbol or address is not provided or cannot be inferred.
        """
        known_symbols: dict[str, str] = known_symbols or {"BTC": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"}

        token_symbol: str | None = self.parameters.get(symbol_key)
        if not token_symbol:
            raise ValueError(f"{token_type.capitalize()} Token Address and Symbol not provided!")

        # Handle known symbol overrides
        if token_symbol in known_symbols:
            self.parameters[address_key] = known_symbols[token_symbol]
            return

        # Infer the token address from the symbol
        self.parameters[address_key] = self._find_key_by_symbol(get_available_tokens(config=self.config), token_symbol)

    def _handle_missing_start_token_address(self) -> None:
        """
        Handles missing 'start_token_address'. Infers the address from the token symbol.
        """
        self._handle_missing_token_address(
            token_type="start", symbol_key="start_token_symbol", address_key="start_token_address"
        )

    def _handle_missing_out_token_address(self) -> None:
        """
        Handles missing 'out_token_address'. Infers the address from the token symbol.
        """
        self._handle_missing_token_address(
            token_type="out", symbol_key="out_token_symbol", address_key="out_token_address"
        )

    def _handle_missing_collateral_address(self) -> None:
        """
        Handles missing 'collateral_address'. Infers the address from the collateral token symbol.

        Validates whether the collateral can be used in the requested market.
        """
        self._handle_missing_token_address(
            token_type="collateral", symbol_key="collateral_token_symbol", address_key="collateral_address"
        )

        # Validate collateral usage
        collateral_address = self.parameters["collateral_address"]
        if self._check_if_valid_collateral_for_market(collateral_address) and self.operation_type != "swap":
            self.parameters["collateral_address"] = collateral_address

    @staticmethod
    def _find_key_by_symbol(input_dict: dict[str, dict[str, str | int | bool]], search_symbol: str) -> str:
        """
        Finds the key in the input dictionary that matches the given token symbol.

        :param input_dict: Dictionary containing token information.
        :param search_symbol: The symbol of the token to search for.
        :return: The key corresponding to the token symbol.
        :raises ValueError: If the token symbol is not found in the input dictionary.
        :return: None
        """
        key: str | None = next((k for k, v in input_dict.items() if v.get("symbol") == search_symbol), None)

        if key is None:
            raise ValueError(f'"{search_symbol}" is not a known token!')

        return key

    def _handle_missing_swap_path(self) -> None:
        """
        Handles missing 'swap_path'. Determines the appropriate swap route based on the operation type
        and the relationship between the start, out, and collateral tokens.

        - If the operation is a token swap, the swap path is calculated between start and out tokens.
        - If the start token matches the collateral token, no swap path is needed.
        - Otherwise, the swap path is determined between the start token and collateral.

        :raises ValueError: If required tokens are missing and cannot determine the swap route.
        :return: None
        """
        start_address: str | None = self.parameters.get("start_token_address")
        out_address: str | None = self.parameters.get("out_token_address")
        collateral_address: str | None = self.parameters.get("collateral_address")

        # Validate that token addresses are present before proceeding
        if not start_address:
            raise ValueError("Start token address is missing!")

        if self.operation_type == "swap":
            if not out_address:
                raise ValueError("Out token address is missing!")
            self.parameters["swap_path"] = self._determine_swap_path(start_address, out_address)
        elif start_address == collateral_address:
            self.parameters["swap_path"] = []
        else:
            if not collateral_address:
                raise ValueError("Collateral token address is missing!")
            self.parameters["swap_path"] = self._determine_swap_path(start_address, collateral_address)

    def _determine_swap_path(self, start_address: str, end_address: str) -> list:
        """
        Determines the swap path between two token addresses using available markets.

        :param start_address: Address of the start token.
        :param end_address: Address of the end token.
        :return: The swap path as a list.
        """
        if not self._available_markets:
            self._available_markets: dict[str, dict[str, Any]] = Markets(self.config).get_available_markets()

        return determine_swap_route(
            config=self.config, markets=self._available_markets, in_token=start_address, out_token=end_address
        )[0]

    def _handle_missing_parameter(self, param_name: str, message: str) -> None:
        """
        General handler for missing parameters.

        :param param_name: The name of the missing parameter.
        :param message: The error message to display when the parameter is missing.
        :raises ValueError: Always raises a ValueError with the provided message.
        :return: None
        """
        raise ValueError(f"Missing parameter: {param_name}. {message}")

    def _handle_missing_is_long(self) -> None:
        """
        Handles the case where 'is_long' is missing from the parameter's dictionary.

        :raises ValueError: If 'is_long' is not provided, which indicates whether the position is long or short.
        :return: None
        """
        self._handle_missing_parameter(
            param_name="is_long",
            message="Please indicate if the position is long ('is_long': True) or short ('is_long': False).",
        )

    def _handle_missing_slippage_percent(self) -> None:
        """
        Handles the case where 'slippage_percent' is missing from the parameter's dictionary.

        :raises ValueError: If 'slippage_percent' is not provided, which is the percentage of acceptable slippage.
        :return: None
        """
        self._handle_missing_parameter(
            param_name="slippage_percent", message="Please provide the slippage percentage ('slippage_percent')."
        )

    def _handle_missing_initial_collateral_delta(self) -> None:
        """
        Handles the case where 'initial_collateral_delta' is missing from the parameter's dictionary.

        :return:
        """
        if "size_delta_usd" in self.parameters and "leverage" in self.parameters:
            collateral_usd: float = self.parameters["size_delta_usd"] / self.parameters["leverage"]
            self.parameters["initial_collateral_delta"] = self._calculate_initial_collateral_tokens(collateral_usd)

    def _check_if_valid_collateral_for_market(self, collateral_address: str) -> bool:
        """
        Checks if the provided collateral address is valid for the requested market.

        :param collateral_address: The address of the collateral token.
        :return: True if valid collateral, otherwise raises a ValueError.
        """
        market_key: str | None = self.parameters.get("market_key")

        # Handle market key overrides directly
        market_key_overrides: dict[str, str] = {
            "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f": "0x47c031236e19d024b42f8AE6780E44A573170703"
        }
        market_key: str | None = market_key_overrides.get(market_key, market_key)

        # Fetch the market information
        if not self._available_markets:
            self._available_markets: dict[str, dict[str, Any]] = Markets(self.config).get_available_markets()
        market: dict | None = self._available_markets.get(market_key)

        if market and (
            collateral_address == market.get("long_token_address")
            or collateral_address == market.get("short_token_address")
        ):
            return True

        logging.error(f"Collateral {collateral_address} is not valid for the selected market.")
        raise ValueError(f"Collateral {collateral_address} is not valid for the selected market.")

    @staticmethod
    def find_key_by_symbol(input_dict: dict, search_symbol: str) -> str:
        """
        Finds the key (token address) in the input_dict that matches the provided symbol.

        :param input_dict: Dictionary of tokens with token symbols as values.
        :param search_symbol: The token symbol to search for.
        :return: The token address corresponding to the symbol.
        :raises ValueError: If the token symbol is not found.
        """
        key: str | None = next((key for key, value in input_dict.items() if value.get("symbol") == search_symbol), None)

        if key is None:
            logging.error(f'"{search_symbol}" not recognized as a valid token.')
            raise ValueError(f'"{search_symbol}" not recognized as a valid token.')

        return key

    @staticmethod
    def find_market_key_by_index_address(input_dict: dict, index_token_address: str) -> str:
        """
        Finds the market key in input_dict based on the index token address.

        :param input_dict: Dictionary of markets with market information.
        :param index_token_address: The index token address to search for.
        :return: The market key corresponding to the index token address.
        :raises ValueError: If the index token address is not found.
        """
        key: str | None = next(
            (key for key, value in input_dict.items() if value.get("index_token_address") == index_token_address), None
        )

        if key is None:
            logging.error(f"Market with index token address {index_token_address} not found.")
            raise ValueError(f"Market with index token address {index_token_address} not found.")

        return key

    def calculate_missing_position_size_info_keys(self) -> dict:
        """
        Calculates missing size-related parameters (e.g., size_delta_usd, initial_collateral_delta)
        if possible. Raises a ValueError if required parameters are missing.

        :raises ValueError: If the required parameters `size_delta_usd`, `initial_collateral_delta`, or `leverage`
            are missing, making the calculations impossible.
        :return: The updated parameters dictionary with `size_delta_usd` and `initial_collateral_delta` filled in, if
            calculated.
        """
        if "size_delta_usd" in self.parameters and "initial_collateral_delta" in self.parameters:
            return self.parameters

        if "leverage" in self.parameters and "initial_collateral_delta" in self.parameters:
            initial_collateral_usd: float = self._calculate_initial_collateral_usd()
            self.parameters["size_delta_usd"] = self.parameters["leverage"] * initial_collateral_usd
            return self.parameters

        if "size_delta_usd" in self.parameters and "leverage" in self.parameters:
            collateral_usd = self.parameters["size_delta_usd"] / self.parameters["leverage"]
            self.parameters["initial_collateral_delta"] = self._calculate_initial_collateral_tokens(collateral_usd)
            return self.parameters

        logging.error('Missing required keys: "size_delta_usd", "initial_collateral_delta", or "leverage".')
        raise ValueError('Missing required keys: "size_delta_usd", "initial_collateral_delta", or "leverage".')

    def _calculate_initial_collateral_usd(self) -> float:
        """
        Calculates the USD value of the collateral from the initial collateral delta.

        :return: The USD value of the initial collateral.
        """
        collateral_amount: float = self.parameters["initial_collateral_delta"]
        prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()
        token_address: str = self.parameters["start_token_address"]

        price: float = float(
            np.median([int(prices[token_address]["maxPriceFull"]), int(prices[token_address]["minPriceFull"])])
        )
        oracle_factor: int = get_available_tokens(config=self.config)[token_address]["decimals"] - 30

        return price * 10**oracle_factor * collateral_amount

    def _calculate_initial_collateral_tokens(self, collateral_usd: float) -> float:
        """
        Calculates the amount of tokens based on the collateral's USD value.

        :param collateral_usd: The dollar value of the collateral.
        :return: The amount of tokens equivalent to the collateral value.
        """
        prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()
        token_address: str = self.parameters["start_token_address"]

        price: float = float(
            np.median([int(prices[token_address]["maxPriceFull"]), int(prices[token_address]["minPriceFull"])])
        )
        oracle_factor: int = get_available_tokens(config=self.config)[token_address]["decimals"] - 30

        return collateral_usd / (price * 10**oracle_factor)

    def _format_size_info(self) -> None:
        """
        Formats size_delta and initial_collateral_delta to the correct precision for on-chain use.
        """
        if self.operation_type != "swap":
            self.parameters["size_delta"] = int(self.parameters["size_delta_usd"] * 10**30)

        decimal: int = get_available_tokens(config=self.config)[self.parameters["start_token_address"]]["decimals"]
        self.parameters["initial_collateral_delta"] = int(self.parameters["initial_collateral_delta"] * 10**decimal)

    def _check_if_max_leverage_exceeded(self):
        """
        Checks if the requested leverage exceeds the maximum allowed leverage.

        :raises ValueError: If the requested leverage exceeds the maximum limit.
        """
        collateral_usd_value: float = self._calculate_initial_collateral_usd()
        leverage_requested: float = self.parameters["size_delta_usd"] / collateral_usd_value

        # TODO: Example value, should be queried from the contract
        max_leverage: float = 100.0
        if leverage_requested > max_leverage:
            error_message: str = (
                f'Requested leverage "x{leverage_requested:.2f}" '
                f"exceeds the maximum allowed leverage of x{max_leverage}."
            )
            logging.error(error_message)
            raise ValueError(error_message)
