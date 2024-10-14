import logging
from logging import Logger
from typing import Any

from web3.contract import Contract
from web3.types import ChecksumAddress, ContractFunction

from pyrfx.config_manager import ConfigManager
from pyrfx.gas_utils import get_gas_limits
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.order.base_order import Order
from pyrfx.utils import get_data_store_contract, get_estimated_swap_output


class SwapOrder(Order):
    """
    A class to handle opening a swap order.
    Extends the base Order class to manage swap logic between tokens in a given market.
    """

    def __init__(
        self,
        start_token: str,
        out_token: str,
        config: ConfigManager,
        market_key: str,
        collateral_address: str,
        index_token_address: str,
        initial_collateral_delta: int,
        slippage_percent: float,
        swap_path: list,
        size_delta: float = 0.0,
        is_long: bool = False,
        max_fee_per_gas: int | None = None,
        auto_cancel: bool = False,
        debug_mode: bool = False,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initialize the SwapOrder class, extending the base Order class.

        :param start_token: Address of the token to swap from.
        :param out_token: Address of the token to swap to.
        :param config: Configuration manager containing blockchain settings.
        :param market_key: The unique key representing the RFX market address.
        :param collateral_address: The contract address of the collateral token.
        :param index_token_address: The contract address of the index token.
        :param initial_collateral_delta: The amount of initial collateral in the order.
        :param slippage_percent: Allowed slippage for the price in percentage.
        :param swap_path: List of contract addresses representing the swap path for token exchanges.
        :param size_delta: Change in position size for the order.
        :param is_long: Boolean indicating whether the order is long or short.
        :param max_fee_per_gas: Optional maximum gas fee to pay per gas unit. If not provided, calculated dynamically.
        :param auto_cancel: Boolean indicating whether the order should be auto-canceled if unfilled.
        :param debug_mode: Boolean indicating whether to run in debug mode (does not submit actual transactions).
        :param log_level: Logging level for this class.
        """
        # Call parent class constructor
        super().__init__(
            config=config,
            market_key=market_key,
            collateral_address=collateral_address,
            index_token_address=index_token_address,
            is_long=is_long,
            size_delta=size_delta,
            initial_collateral_delta=initial_collateral_delta,
            slippage_percent=slippage_percent,
            order_type="swap",
            swap_path=swap_path,
            max_fee_per_gas=max_fee_per_gas,
            auto_cancel=auto_cancel,
            debug_mode=debug_mode,
            log_level=log_level,
        )

        # Set start and out token addresses
        self.start_token: str = start_token
        self.out_token: str = out_token

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        # Determine gas limits
        self.determine_gas_limits()

    def determine_gas_limits(self) -> None:
        """
        Determine the gas limits required for placing a swap order.

        This method queries the datastore contract to get the relevant gas limits and
        sets the gas limit for the swap operation.
        """
        try:
            # Retrieve the datastore contract
            datastore: Contract = get_data_store_contract(self.config)

            if not datastore:
                raise ValueError("Datastore contract was not found.")

            # Fetch the gas limits from the datastore
            self._gas_limits: dict[str, ContractFunction] = get_gas_limits(datastore)

            if not self._gas_limits:
                raise ValueError("Gas limits could not be retrieved.")

            # Retrieve the specific gas limit for the 'swap_order' operation
            self._gas_limits_order_type_contract_function: ContractFunction | None = self._gas_limits.get("swap_order")

            if not self._gas_limits_order_type_contract_function:
                raise KeyError("Gas limit for 'swap_order' not found.")

            if self.debug_mode:
                # Get the actual gas limit value by calling the contract function
                gas_limit_value: int = self._gas_limits_order_type_contract_function.call()
                self.logger.info(f"Gas limit for 'swap_order' is: {gas_limit_value}")

        except KeyError as e:
            self.logger.error(f"KeyError - Gas limit for 'swap_order' not found: {e}")
            raise Exception(f"Gas limit for 'swap_order' not found: {e}")

        except ValueError as e:
            self.logger.error(f"ValueError - Issue with datastore or gas limits: {e}")
            raise Exception(f"Error with datastore or gas limits: {e}")

        except Exception as e:
            self.logger.error(f"Unexpected error while determining gas limits: {e}")
            raise Exception(f"Unexpected error while determining gas limits: {e}")

    def estimated_swap_output(self, market: dict[str, Any], in_token: str, in_token_amount: int) -> dict[str, Any]:
        """
        Estimate the output of a token swap given a market and input token amount.

        :param market: Full market details containing token addresses and metadata.
        :param in_token: Contract address of the input token.
        :param in_token_amount: Amount of input token to swap.
        :return: A dictionary containing the estimated token output and price impact.
        """
        try:
            # Convert token addresses to checksum format
            in_token_address: ChecksumAddress = self.config.to_checksum_address(address=in_token)

            # Fetch recent prices from the Oracle
            prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()

            # Prepare the swap estimation parameters
            swap_parameters: dict[str, Any] = self._prepare_swap_parameters(
                market=market, prices=prices, in_token_address=in_token_address, in_token_amount=in_token_amount
            )

            # Get estimated swap output
            estimated_output: dict[str, int | float] = get_estimated_swap_output(
                config=self.config, params=swap_parameters
            )

            self.logger.info(f"Estimated swap output: {estimated_output}")
            return estimated_output

        except KeyError as e:
            self.logger.error(f"Missing data in swap output estimation parameters: {e}")
            return {"out_token_amount": 0, "price_impact_usd": 0}

        except Exception as e:
            self.logger.error(f"Unexpected error while estimating swap output: {e}")
            return {"out_token_amount": 0, "price_impact_usd": 0}

    def _prepare_swap_parameters(
        self,
        market: dict[str, Any],
        prices: dict[str, dict[str, int]],
        in_token_address: ChecksumAddress,
        in_token_amount: int,
    ) -> dict[str, Any]:
        """
        Helper method to prepare the parameters for the swap estimation.

        :param market: Full market details containing token addresses and metadata.
        :param prices: Recent prices for tokens from the Oracle.
        :param in_token_address: The checksum address of the input token.
        :param in_token_amount: Amount of input token to swap.
        :return: A dictionary of parameters required for the swap estimation.
        """
        return {
            "data_store_address": self.config.contracts.data_store.contract_address,
            "market_addresses": [
                market["rfx_market_address"],
                market["index_token_address"],
                market["long_token_address"],
                market["short_token_address"],
            ],
            "token_prices_tuple": [
                [
                    int(prices[market["index_token_address"]]["maxPriceFull"]),
                    int(prices[market["index_token_address"]]["minPriceFull"]),
                ],
                [
                    int(prices[market["long_token_address"]]["maxPriceFull"]),
                    int(prices[market["long_token_address"]]["minPriceFull"]),
                ],
                [
                    int(prices[market["short_token_address"]]["maxPriceFull"]),
                    int(prices[market["short_token_address"]]["minPriceFull"]),
                ],
            ],
            "token_in": in_token_address,
            "token_amount_in": in_token_amount,
            # TODO: Placeholder for ui_fee_receiver
            "ui_fee_receiver": self.config.zero_address,
        }
