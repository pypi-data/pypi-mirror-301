import logging
from logging import Logger
from typing import Any

import numpy as np

from pyrfx.config_manager import ConfigManager
from pyrfx.get.markets import Markets
from pyrfx.get.oracle_prices import OraclePrices
from pyrfx.keys import pool_amount_key
from pyrfx.utils import get_data_store_contract, save_csv, save_json, timestamp_df


class GetPoolTVL:
    """
    A class to retrieve and calculate the Total Value Locked (TVL) in USD across all pools
    for a specified blockchain.
    """

    def __init__(self, config: ConfigManager, log_level: int = logging.INFO) -> None:
        """
        Initialize the GetPoolTVL class with the given chain configuration.

        :param config: ConfigManager object containing the chain configuration.
        :param log_level: Logging level for this class.
        """
        self.config: ConfigManager = config

        # Setup logger
        self.logger: Logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        # Load oracle prices
        self._prices: dict[str, dict[str, Any]] = OraclePrices(config=self.config).get_recent_prices()

        # Initialize datastore
        self.datastore: Any = get_data_store_contract(self.config)

    def get_pool_balances(self) -> dict[str, dict[str, Any]]:
        """
        Get the total USD balances across all pools for the defined chain.

        :return: Dictionary containing pool data including TVL.
        """
        markets: dict[str, dict[str, Any]] = Markets(self.config).get_available_markets()
        pool_tvl: dict[str, dict[str, Any]] = {"total_tvl": {}, "long_token": {}, "short_token": {}}

        for market_key, market_data in markets.items():
            market_symbol: str = market_data["market_symbol"]

            long_token_metadata: dict[str, Any] = market_data["long_token_metadata"]
            short_token_metadata: dict[str, Any] = market_data["short_token_metadata"]

            long_token_balance, short_token_balance = self._query_balances(
                market_key, long_token_metadata["address"], short_token_metadata["address"]
            )

            long_usd_balance: float = self._calculate_usd_value(
                long_token_metadata["address"], long_token_balance, long_token_metadata["decimals"]
            )
            short_usd_balance: float = self._calculate_usd_value(
                short_token_metadata["address"], short_token_balance, short_token_metadata["decimals"]
            )

            pool_tvl["total_tvl"][market_symbol] = long_usd_balance + short_usd_balance
            pool_tvl["long_token"][market_symbol] = long_token_metadata["address"]
            pool_tvl["short_token"][market_symbol] = short_token_metadata["address"]
            self.logger.info(f"{market_symbol:4} | Total pool value: ${long_usd_balance + short_usd_balance:,.2f}")

        if self.config.save_to_json:
            file_name: str = f"{self.config.chain}_pool_tvl.json"
            save_json(output_data_path=self.config.data_path, file_name=file_name, data=pool_tvl)
            self.logger.info(f"Data saved as JSON: {file_name}")

        if self.config.save_to_csv:
            file_name: str = f"{self.config.chain}_total_tvl.csv"
            save_csv(
                output_data_path=self.config.data_path, file_name=file_name, data=timestamp_df(pool_tvl["total_tvl"])
            )
            self.logger.info(f"Data saved as CSV: {file_name}")

        return pool_tvl

    def _query_balances(self, market: str, long_token_address: str, short_token_address: str) -> tuple[int, int]:
        """
        Query the long and short token balances for a given market.

        :param market: RFX market address.
        :param long_token_address: Long token address.
        :param short_token_address: Short token address.
        :return: Tuple containing long and short token balances.
        """
        long_token_balance: int = self._get_token_balance(market, long_token_address)
        short_token_balance: int = self._get_token_balance(market, short_token_address)
        return long_token_balance, short_token_balance

    def _get_token_balance(self, market: str, token_address: str) -> int:
        """
        Retrieve the balance for a specific token in a given market from the datastore.

        :param market: RFX market address.
        :param token_address: Token address.
        :return: Token balance.
        """
        pool_amount_hash_data: bytes = pool_amount_key(market, token_address)
        return self.datastore.functions.getUint(pool_amount_hash_data).call()

    def _calculate_usd_value(self, token_address: str, token_balance: int, decimals: int) -> float:
        """
        Calculate the USD value for a token balance based on recent oracle prices.

        :param token_address: Address of the token.
        :param token_balance: Balance of the token.
        :param decimals: Decimal precision of the token.
        :return: USD value of the token balance.
        """
        try:
            oracle_precision: int = 10 ** (30 - decimals)
            token_price: float = float(
                np.median(
                    [
                        float(self._prices[token_address]["maxPriceFull"]) / oracle_precision,
                        float(self._prices[token_address]["minPriceFull"]) / oracle_precision,
                    ]
                )
            )
            return token_price * token_balance / 10**decimals
        except KeyError:
            self.logger.error(f"Token address {token_address} not found in oracle prices.")
            return token_balance / 10**decimals
