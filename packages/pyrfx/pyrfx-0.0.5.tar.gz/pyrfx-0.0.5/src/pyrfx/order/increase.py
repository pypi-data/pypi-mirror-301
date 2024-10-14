import logging
from logging import Logger
from typing import Any

from web3.contract import Contract
from web3.contract.contract import ContractFunction

from pyrfx.config_manager import ConfigManager
from pyrfx.gas_utils import get_gas_limits
from pyrfx.order.base_order import Order
from pyrfx.utils import get_data_store_contract


class IncreaseOrder(Order):
    """
    A class to handle opening a buy order on the blockchain.
    Extends the base Order class to manage the logic for increasing (buy) orders.
    """

    def __init__(
        self,
        config: ConfigManager,
        market_key: str,
        collateral_address: str,
        index_token_address: str,
        is_long: bool,
        size_delta: float,
        initial_collateral_delta: int,
        slippage_percent: float,
        swap_path: list | None = None,
        max_fee_per_gas: int | None = None,
        auto_cancel: bool = False,
        debug_mode: bool = False,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initialize the IncreaseOrder class, extending the base Order class.

        :param config: Configuration manager containing blockchain settings.
        :param market_key: The unique key representing the RFX market address.
        :param collateral_address: The contract address of the collateral token.
        :param index_token_address: The contract address of the index token.
        :param is_long: Boolean indicating whether the order is long or short.
        :param size_delta: Change in position size for the order.
        :param initial_collateral_delta: The amount of initial collateral in the order.
        :param slippage_percent: Allowed slippage for the price in percentage.
        :param swap_path: List of contract addresses representing the swap path for token exchanges.
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
            order_type="increase",
            swap_path=swap_path,
            max_fee_per_gas=max_fee_per_gas,
            auto_cancel=auto_cancel,
            debug_mode=debug_mode,
            log_level=log_level,
        )

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        # Determine gas limits
        self.determine_gas_limits()

    def determine_gas_limits(self) -> None:
        """
        Determine the gas limits required for placing an increase (buy) order.

        This method queries the datastore contract to get the relevant gas limits
        and sets the gas limit for the increase order operation.

        Logs an error if gas limits cannot be retrieved or if any other exception occurs.
        """
        try:
            # Retrieve the datastore contract
            datastore: Contract = get_data_store_contract(self.config)

            if not datastore:
                raise ValueError("Datastore contract was not found.")

            # Fetch the gas limits from the datastore
            self._gas_limits: dict[str, Any] = get_gas_limits(datastore)

            if not self._gas_limits:
                raise ValueError("Gas limits could not be retrieved.")

            # Retrieve the specific gas limit for the 'increase_order' operation
            self._gas_limits_order_type_contract_function: ContractFunction | None = self._gas_limits.get(
                "increase_order"
            )

            if not self._gas_limits_order_type_contract_function:
                raise KeyError("Gas limit for 'increase_order' not found.")

            if self.debug_mode:
                # Get the actual gas limit value by calling the contract function
                gas_limit_value: int = self._gas_limits_order_type_contract_function.call()
                self.logger.info(f"Gas limit for 'increase_order' is: {gas_limit_value}")

        except KeyError as e:
            self.logger.error(f"KeyError - Gas limit for 'increase_order' not found: {e}")
            raise Exception(f"Gas limit for 'increase_order' not found: {e}")

        except ValueError as e:
            self.logger.error(f"ValueError - Issue with datastore or gas limits: {e}")
            raise Exception(f"Error with datastore or gas limits: {e}")

        except Exception as e:
            self.logger.error(f"Unexpected error while determining gas limits: {e}")
            raise Exception(f"Unexpected error while determining gas limits: {e}")
