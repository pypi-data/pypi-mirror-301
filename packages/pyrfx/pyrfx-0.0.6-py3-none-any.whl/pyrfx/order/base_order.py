import logging
from abc import ABC, abstractmethod
from logging import Logger
from typing import Any

import numpy as np
from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
from web3.contract import Contract
from web3.contract.contract import ContractFunction
from web3.types import BlockData, ChecksumAddress, TxParams

from pyrfx.approve_token_for_spend import check_if_approved
from pyrfx.config_manager import ConfigManager
from pyrfx.gas_utils import get_execution_fee
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.utils import (
    PRECISION,
    DecreasePositionSwapTypes,
    OrderTypes,
    get_exchange_router_contract,
    get_execution_price_and_price_impact,
)


class Order(ABC):
    """
    A class to handle the creation, approval, and submission of orders.
    Handles different types of orders such as buy, sell, and swap with configurable gas fees, slippage, and collateral.
    """

    @abstractmethod
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
        order_type: str,
        swap_path: list | None,
        max_fee_per_gas: int | None = None,
        auto_cancel: bool = False,
        debug_mode: bool = False,
        log_level: int = logging.INFO,
    ) -> None:
        """
        Initializes the Order class with the provided parameters and handles default behavior.

        :param config: Configuration manager containing blockchain settings.
        :param market_key: The unique key representing the RFX market address.
        :param collateral_address: The contract address of the collateral token.
        :param index_token_address: The contract address of the index token.
        :param is_long: Boolean indicating whether the order is long or short.
        :param size_delta: Change in position size for the order.
        :param initial_collateral_delta: The amount of initial collateral in the order.
        :param slippage_percent: Allowed slippage for the price in percentage.
        :param order_type: The type of order to create.
        :param swap_path: List of contract addresses representing the swap path for token exchanges.
        :param max_fee_per_gas: Optional maximum gas fee to pay per gas unit. If not provided, calculated dynamically.
        :param auto_cancel: Boolean indicating whether the order should be auto-canceled if unfilled.
        :param debug_mode: Boolean indicating whether to run in debug mode (does not submit actual transactions).
        :param log_level: Logging level for this class.
        """
        self.config: ConfigManager = config
        self.market_key: str = market_key
        self.collateral_address: str = collateral_address
        self.index_token_address: str = index_token_address
        self.is_long: bool = is_long
        self.size_delta: float = size_delta
        self.initial_collateral_delta: int = initial_collateral_delta
        self.slippage_percent: float = slippage_percent
        self.order_type: str = order_type
        self.swap_path: list | None = swap_path
        self.max_fee_per_gas: int | None = max_fee_per_gas
        self.auto_cancel: bool = auto_cancel
        self.debug_mode: bool = debug_mode

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        self._gas_limits: dict = {}
        self._gas_limits_order_type_contract_function: ContractFunction | None = None

        # Dynamically calculate max_fee_per_gas if not provided
        if self.max_fee_per_gas is None:
            block: BlockData = self.config.connection.eth.get_block("latest")
            self.max_fee_per_gas: int = int(block["baseFeePerGas"] * 1.35)

        self._exchange_router_contract_obj: Contract = get_exchange_router_contract(config=self.config)

    @abstractmethod
    def determine_gas_limits(self) -> None:
        """
        Determine and set gas limits for the order.
        This method is meant to be overridden by subclasses if custom gas limits are required.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def estimated_swap_output(self, market: dict[str, Any], in_token: str, in_token_amount: int) -> dict[str, Any]:
        """
        Estimate the output of a token swap given a market and input token amount.

        :param market: Full market details containing token addresses and metadata.
        :param in_token: Contract address of the input token.
        :param in_token_amount: Amount of input token to swap.
        :return: A dictionary containing the estimated token output and price impact.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def create_and_execute(self) -> None:
        """
        Build and submit an order, determining whether it is an open, close, or swap order, and ensuring correct gas
        limits, fees, and execution parameters are set.

        :raises Exception: If the execution price falls outside the acceptable range for the order type.
        """

        # Set gas limits and execution fee
        self.determine_gas_limits()
        gas_price: int = self.config.connection.eth.gas_price
        execution_fee: int = int(
            get_execution_fee(
                gas_limits=self._gas_limits,
                estimated_gas_limit_contract_function=self._gas_limits_order_type_contract_function,
                gas_price=gas_price,
            )
        )

        # Check approval if not closing and not in debug mode
        if self.order_type == "decrease" and not self.debug_mode:
            check_if_approved(
                config=self.config,
                spender_address=self.config.contracts.synthetics_router.contract_address,
                token_to_approve_address=self.collateral_address,
                amount_of_tokens_to_spend=self.initial_collateral_delta,
                max_fee_per_gas=self.max_fee_per_gas,
                approve=True,
                logger=self.logger,
            )

        # Adjust execution fee for swap orders due to complexity
        execution_fee_multiplier: float = 1.5 if self.order_type == "swap" else 1.2
        execution_fee: int = int(execution_fee * execution_fee_multiplier)

        markets: dict[str, dict[str, Any]] = Markets(config=self.config).get_available_markets()
        prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()
        size_delta_price_price_impact: float = self.size_delta

        # Adjust size_delta for closing positions (negative impact)
        if self.order_type == "decrease":
            size_delta_price_price_impact *= -1

        # Set callback gas limit and minimum output amount
        callback_gas_limit: int = 0
        min_output_amount: int = 0

        # Determine the type of order: increase, decrease, or swap
        order_type_value: int | None = None
        if self.order_type == "increase":
            order_type_value: int = OrderTypes.MARKET_INCREASE.value
        elif self.order_type == "decrease":
            order_type_value: int = OrderTypes.MARKET_DECREASE.value
        elif self.order_type == "swap":
            order_type_value: int = OrderTypes.MARKET_SWAP.value

            # Estimate the output token amount for the swap
            estimated_output = self.estimated_swap_output(
                market=markets[self.swap_path[0]],
                in_token=self.collateral_address,
                in_token_amount=self.initial_collateral_delta,
            )

            # Adjust gas limits and estimate output for multi-swap paths
            self._gas_limits_order_type_contract_function: ContractFunction = self._gas_limits["single_swap"]
            if len(self.swap_path) > 1:
                estimated_output = self.estimated_swap_output(
                    market=markets[self.swap_path[1]],
                    # Example intermediate token, USDC
                    in_token=self.config.usdc_address,
                    in_token_amount=int(
                        estimated_output["out_token_amount"]
                        - estimated_output["out_token_amount"] * self.slippage_percent
                    ),
                )
                self._gas_limits_order_type_contract_function: ContractFunction = self._gas_limits["swap_order"]

            min_output_amount: int = int(
                estimated_output["out_token_amount"] - estimated_output["out_token_amount"] * self.slippage_percent
            )

        should_unwrap_native_token: bool = True
        referral_code: HexBytes = HexBytes("0x0000000000000000000000000000000000000000000000000000000000000000")

        # Ensure wallet addresses are converted to checksum format
        eth_zero_address: ChecksumAddress = self.config.zero_address
        ui_ref_address: ChecksumAddress = self.config.zero_address
        collateral_address: ChecksumAddress = self.config.to_checksum_address(address=self.collateral_address)

        # Convert market key to checksum address
        rfx_market_address: ChecksumAddress = self.config.to_checksum_address(address=self.market_key)

        # Parameters for calculating the execution price
        execution_price_parameters: dict[str, Any] = {
            "data_store_address": self.config.contracts.data_store.contract_address,
            "market_key": self.market_key,
            "index_token_price": [
                int(prices[self.index_token_address]["maxPriceFull"]),
                int(prices[self.index_token_address]["minPriceFull"]),
            ],
            "position_size_in_usd": 0,
            "position_size_in_tokens": 0,
            "size_delta": size_delta_price_price_impact,
            "is_long": self.is_long,
        }

        # Retrieve market details and calculate price based on slippage
        decimals: int = markets[self.market_key]["market_metadata"]["decimals"]
        price, acceptable_price, acceptable_price_in_usd = self._get_prices(decimals=decimals, prices=prices)

        # Set mark price for open positions
        mark_price: int = int(price) if self.order_type == "increase" else 0

        # For swap orders, acceptable price and market address are not relevant
        if self.order_type == "swap":
            acceptable_price: int = 0
            rfx_market_address: ChecksumAddress = self.config.zero_address

        # Calculate execution price and its impact
        execution_price_and_price_impact: dict = get_execution_price_and_price_impact(
            config=self.config, params=execution_price_parameters, decimals=decimals
        )
        self.logger.info(f"Execution price: ${execution_price_and_price_impact['execution_price']:.4f}")

        # Check if execution price is within acceptable range
        if self.order_type == "increase":
            if (self.is_long and execution_price_and_price_impact["execution_price"] > acceptable_price_in_usd) or (
                not self.is_long and execution_price_and_price_impact["execution_price"] < acceptable_price_in_usd
            ):
                raise Exception("Execution price falls outside the acceptable range!")
        elif self.order_type == "decrease":
            if (self.is_long and execution_price_and_price_impact["execution_price"] < acceptable_price_in_usd) or (
                not self.is_long and execution_price_and_price_impact["execution_price"] > acceptable_price_in_usd
            ):
                raise Exception("Execution price falls outside the acceptable range!")

        # Build the order arguments
        arguments: tuple = (
            (
                self.config.user_wallet_address,
                self.config.user_wallet_address,  # Cancellation receiver
                eth_zero_address,
                ui_ref_address,
                rfx_market_address,
                collateral_address,
                self.swap_path,
            ),
            (
                self.size_delta,
                self.initial_collateral_delta,
                mark_price,
                acceptable_price,
                execution_fee,
                callback_gas_limit,
                int(min_output_amount),
            ),
            order_type_value,
            DecreasePositionSwapTypes.NO_SWAP.value,
            self.is_long,
            should_unwrap_native_token,
            self.auto_cancel,
            referral_code,
        )

        # If the collateral is not a native token (e.g., ETH or AVAX), send tokens to the vault
        value_amount: int = execution_fee
        if self.collateral_address != self.config.weth_address and not self.order_type == "decrease":
            multicall_args: list[HexBytes] = [
                HexBytes(self._send_wnt(value_amount)),
                HexBytes(self._send_tokens(self.collateral_address, self.initial_collateral_delta)),
                HexBytes(self._create_order(arguments)),
            ]
        else:
            # For open or swap orders involving native tokens, send both tokens and execution fee
            if self.order_type == "increase" or self.order_type == "swap":
                value_amount += self.initial_collateral_delta
            multicall_args: list[HexBytes] = [
                HexBytes(self._send_wnt(value_amount)),
                HexBytes(self._create_order(arguments)),
            ]

        # Submit the transaction
        self._submit_transaction(
            user_wallet_address=self.config.user_wallet_address,
            value_amount=value_amount,
            multicall_args=multicall_args,
        )

    def _submit_transaction(
        self, user_wallet_address: ChecksumAddress, value_amount: float, multicall_args: list
    ) -> None:
        """
        Builds and submits the transaction to the network.

        :param user_wallet_address: The wallet address submitting the transaction.
        :param value_amount: The amount of value (in native tokens) to send along with the transaction.
        :param multicall_args: List of arguments for multicall operations in the transaction.
        """
        self.logger.info("Building transaction ...")

        nonce: int = self.config.connection.eth.get_transaction_count(user_wallet_address)

        raw_txn: TxParams = self._exchange_router_contract_obj.functions.multicall(multicall_args).build_transaction(
            {
                "value": value_amount,
                "chainId": self.config.chain_id,
                "gas": (2 * self._gas_limits_order_type_contract_function.call()),
                "maxFeePerGas": int(self.max_fee_per_gas),
                "maxPriorityFeePerGas": 0,
                "nonce": nonce,
            }
        )

        if not self.debug_mode:
            signed_txn: SignedTransaction = self.config.connection.eth.account.sign_transaction(
                raw_txn, self.config.private_key
            )
            tx_hash: HexBytes = self.config.connection.eth.send_raw_transaction(signed_txn.rawTransaction)

            tx_url: str = f"{self.config.block_explorer_url}/tx/{tx_hash.hex()}"
            self.logger.info(f"Transaction submitted! HEX: {tx_hash.hex()}")
            self.logger.info(f"Transaction submitted! Check status: {tx_url}")

    def _get_prices(self, decimals: float, prices: dict) -> tuple[float, int, float]:
        """
        Retrieves and calculates the acceptable prices for the order based on current market conditions and slippage.

        :param decimals: Decimal precision for the token.
        :param prices: Dictionary containing min and max prices from the Oracle.
        :return: A tuple containing the median price, slippage-adjusted price, and acceptable price in USD.
        """
        self.logger.info("Fetching current prices ...")

        price: float = float(
            np.median(
                [
                    float(prices[self.index_token_address]["maxPriceFull"]),
                    float(prices[self.index_token_address]["minPriceFull"]),
                ]
            )
        )

        if self.order_type == "increase":
            slippage = int(price * (1 + self.slippage_percent if self.is_long else 1 - self.slippage_percent))
        elif self.order_type == "decrease":
            slippage = int(price * (1 - self.slippage_percent if self.is_long else 1 + self.slippage_percent))
        else:
            slippage = int(price)

        acceptable_price_in_usd: float = slippage * 10 ** (decimals - PRECISION)

        self.logger.info(f"Mark Price: ${price * 10 ** (decimals - PRECISION):.4f}")
        self.logger.info(f"Acceptable price: ${acceptable_price_in_usd:.4f}")

        return price, slippage, acceptable_price_in_usd

    def _create_order(self, arguments: tuple) -> str:
        """
        Create an order by encoding the contract function call.

        :param arguments: A tuple containing the necessary parameters for creating the order, such as wallet addresses,
                          market details, collateral amounts, and execution fees.
        :return: The ABI-encoded string representing the 'createOrder' contract function call.
        """
        return self._exchange_router_contract_obj.functions.createOrder.encodeABI([arguments])

    def _send_tokens(self, token_address: str, amount: int) -> str:
        """
        Send tokens to the exchange contract.

        :param token_address: The address of the token to send.
        :param amount: The amount of tokens to send.
        :return: The ABI-encoded string representing the 'sendTokens' contract function call.
        """
        return self._exchange_router_contract_obj.functions.sendTokens.encodeABI(
            token_address, self.config.contracts.order_vault.contract_address, amount
        )

    def _send_wnt(self, amount: int) -> str:
        """
        Send Wrapped Native Token (WNT) to the exchange contract.

        :param amount: The amount of WNT to send.
        :return: The ABI-encoded string representing the 'sendWnt' contract function call.
        """
        return self._exchange_router_contract_obj.functions.sendWnt.encodeABI(
            self.config.contracts.order_vault.contract_address, amount
        )
