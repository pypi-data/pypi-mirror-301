import logging
from typing import Any

import numpy as np

from pyrfx.config_manager import ConfigManager
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.utils import get_available_tokens


class LiquidityArgumentParser:
    """
    A utility class to parse and process liquidity arguments for deposit and withdrawal orders.
    This class ensures that all required parameters are present and properly formatted.
    """

    def __init__(self, config: ConfigManager, operation_type: str) -> None:
        """
        Initialize the LiquidityArgumentParser with necessary configurations and parameters.

        :param config: Configuration object containing chain and market settings.
        :param operation_type: The type of operation to be performed, either 'deposit' or 'withdraw'.
        :raises ValueError: If the operation_type is not 'deposit' or 'withdraw'.
        """
        self.config: ConfigManager = config
        self.operation_type: str = operation_type
        self.parameters: dict = {}
        self._allowed_operation_types: list[str] = ["deposit", "withdraw"]

        if self.operation_type not in self._allowed_operation_types:
            error_message: str = (
                f'Operation type {operation_type} is not valid. Valid types: {", ".join(self._allowed_operation_types)}'
            )
            logging.error(error_message)
            raise ValueError(error_message)

        # Cache token addresses dictionary to avoid repeated lookups
        self.available_tokens: dict[str, dict[str, str | int | bool]] = get_available_tokens(config=self.config)

        # Set required keys based on operation type
        self.required_keys: list[str] = self._set_required_keys()

        self.missing_base_key_methods: dict = {
            "market_key": self._handle_missing_market_key,
            "long_token_address": self._handle_missing_long_token_address,
            "short_token_address": self._handle_missing_short_token_address,
            "long_token_amount": self._handle_missing_long_token_amount,
            "short_token_amount": self._handle_missing_short_token_amount,
            "out_token_address": self._handle_missing_out_token_address,
        }

    def process_parameters(self, parameters: dict[str, Any]) -> dict[str, Any]:
        """
        Process and validate the input parameters, ensuring all required keys are present.
        If a key is missing, the corresponding handler is called to resolve it.

        :param parameters: Dictionary containing the necessary parameters.
        :return: A fully populated and validated parameter's dictionary.
        """
        self.parameters: dict = parameters
        missing_keys: list = self._determine_missing_keys(parameters)

        for missing_key in missing_keys:
            if missing_key in self.missing_base_key_methods:
                self.missing_base_key_methods[missing_key]()

        if self.operation_type == "withdraw":
            self.parameters["rm_amount"] = int(self.parameters["rm_amount"] * 10**18)

        return self.parameters

    def _set_required_keys(self) -> list[str]:
        """
        Set the list of required keys based on the operation type (deposit or withdrawal).

        :return: A list of required keys for the specified operation.
        """
        if self.operation_type == "deposit":
            return [
                "market_key",
                "long_token_address",
                "short_token_address",
                "long_token_amount",
                "short_token_amount",
            ]
        elif self.operation_type == "withdraw":
            return ["market_key", "out_token_address", "rm_amount"]
        else:
            return []

    def _determine_missing_keys(self, parameters: dict[str, Any]) -> list[str]:
        """
        Compare the provided parameters against the required keys for the operation.

        :param parameters: Dictionary of user-supplied parameters.
        :return: A list of missing keys.
        """
        return [key for key in self.required_keys if key not in parameters]

    def _handle_missing_index_token_address(self) -> None:
        """
        Handle missing index token address by attempting to find it via the market token symbol.

        :raises ValueError: If the market token address and symbol are not provided.
        """
        # Retrieve market token symbol from parameters
        token_symbol: str | None = self.parameters.get("market_token_symbol")
        if not token_symbol:
            logging.error("Market token symbol is not provided in parameters.")
            raise ValueError("Market token symbol is not provided in parameters.")

        self.parameters["market_token_address"] = self.find_token_address_by_symbol(
            tokens=self.available_tokens, symbol=token_symbol
        )

    def _handle_missing_market_key(self) -> None:
        """
        Handle missing market key by using the index token address.

        :raises ValueError: If the market token address and symbol are not provided.
        """
        self._handle_missing_index_token_address()
        self.parameters["market_key"] = self.find_market_by_address(
            markets=Markets(self.config).get_available_markets(),
            token_address=self.parameters["market_token_address"],
        )

    def _handle_missing_token_address(self, token_type: str) -> None:
        """
        General handler for missing token addresses (long/short).

        :param token_type: Either 'long' or 'short' to indicate which token is being processed.
        """
        token_symbol: str | None = self.parameters.get(f"{token_type}_token_symbol")
        if not token_symbol:
            logging.error(f"{token_type.capitalize()} token symbol is not provided in parameters.")
            raise ValueError(f"{token_type.capitalize()} token symbol is not provided.")

        if token_symbol.upper() == "BTC":
            self.parameters[f"{token_type}_token_address"] = "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"
        else:
            self.parameters[f"{token_type}_token_address"] = self.find_token_address_by_symbol(
                tokens=self.available_tokens, symbol=token_symbol
            )

    def _handle_missing_long_token_address(self) -> None:
        """
        Handle missing long token address by searching with the token symbol.
        """
        self._handle_missing_token_address(token_type="long")

    def _handle_missing_short_token_address(self) -> None:
        """
        Handle missing short token address by searching with the token symbol.
        """
        self._handle_missing_token_address(token_type="short")

    def _handle_missing_out_token_address(self) -> None:
        """
        Handle missing out token address by searching with the token symbol.

        :raises ValueError: If the out token address or symbol is not provided.
        """
        # Get long token symbol, raise an error if not provided
        long_token_symbol: str | None = self.parameters.get("long_token_symbol")
        if not long_token_symbol:
            logging.error("Long token symbol is not provided.")
            raise ValueError("Long token symbol is not provided.")

        # Special case for "BTC" token symbol
        if long_token_symbol == "BTC":
            self.parameters["long_token_address"] = "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"
            return

        self.parameters["long_token_address"] = self.find_token_address_by_symbol(
            tokens=self.available_tokens, symbol=long_token_symbol
        )

    def _handle_missing_token_amount(self, token_type: str, usd_key: str) -> None:
        """
        Generic handler for missing long or short token amounts.

        :param token_type: Either 'long' or 'short' indicating the token type.
        :param usd_key: The key for USD value in the parameters.
        """
        token_address: str | None = self.parameters.get(f"{token_type}_token_address")
        if not token_address:
            self.parameters[f"{token_type}_token_amount"] = 0
            return

        prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()
        price_data: dict | None = prices.get(token_address)

        if not price_data:
            logging.error(f"Price data not found for {token_type} token address: {token_address}")
            raise ValueError(f"Price data not found for {token_type} token address: {token_address}")

        price: float = float(np.median([float(price_data["maxPriceFull"]), float(price_data["minPriceFull"])]))

        # Calculate amount
        decimal: int = self.available_tokens.get(token_address, {}).get("decimals", 18)
        oracle_factor: int = decimal - 30
        adjusted_price: float = price * 10**oracle_factor
        token_usd: float = self.parameters.get(usd_key, 0)
        self.parameters[f"{token_type}_token_amount"] = int((token_usd / adjusted_price) * 10**decimal)

    def _handle_missing_long_token_amount(self) -> None:
        """
        Handle missing long token amount by calculating it based on the USD value.

        :raises ValueError: If the long token address is not provided.
        """
        self._handle_missing_token_amount(token_type="long", usd_key="long_token_usd")

    def _handle_missing_short_token_amount(self) -> None:
        """
        Handle missing short token amount by calculating it based on the USD value.

        :raises ValueError: If the short token address is not provided or price data is missing.
        """
        self._handle_missing_token_amount(token_type="short", usd_key="short_token_usd")

    @staticmethod
    def find_token_address_by_symbol(tokens: dict, symbol: str) -> str:
        """
        Find the token contract address by its symbol.

        :param tokens: Dictionary containing token information.
        :param symbol: The token symbol to search for.
        :return: The contract address of the token.
        :raises ValueError: If the token symbol is not found.
        """
        token_address: str | None = next((key for key, value in tokens.items() if value.get("symbol") == symbol), None)

        if not token_address:
            error_message: str = (
                f"Token address was not found for the symbol: {symbol}. Please check if the symbol is correct."
            )
            logging.error(error_message)
            raise ValueError(error_message)

        return token_address

    @staticmethod
    def find_market_by_address(markets: dict, token_address: str) -> str:
        """
        Find the market key by index token address.

        :param markets: Dictionary containing market information.
        :param token_address: The index token address to search for.
        :return: The market key corresponding to the index token, or None if not found.
        """
        market: str | None = next(
            (key for key, value in markets.items() if value.get("index_token_address") == token_address), None
        )

        if not market:
            logging.error(f"Market address was not found for token address: {token_address}")
            raise ValueError(f"Market address was not found for token address: {token_address}")

        return market
