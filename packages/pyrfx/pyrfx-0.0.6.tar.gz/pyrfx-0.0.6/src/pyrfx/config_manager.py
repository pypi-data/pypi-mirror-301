import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from web3 import Web3
from web3.types import ChecksumAddress


@dataclass
class ContractInfo:
    """
    Represents the information for a smart contract, including its address and the path to its ABI.
    """

    contract_address: ChecksumAddress
    abi_path: str


@dataclass
class NetworkContracts:
    """
    Holds contract information for various contract types within a given blockchain network.
    """

    data_store: ContractInfo
    event_emitter: ContractInfo
    exchange_router: ContractInfo
    deposit_vault: ContractInfo
    withdrawal_vault: ContractInfo
    order_vault: ContractInfo
    synthetics_reader: ContractInfo
    synthetics_router: ContractInfo

    def __getitem__(self, contract_name: str) -> ContractInfo | None:
        """
        Allow dictionary-style access to the contracts by contract name.

        :param contract_name: The name of the contract to access (e.g., 'data_store', 'event_emitter').
        :return: The ContractInfo associated with the contract name or None if not found.
        """
        return getattr(self, contract_name, None)


# Default chain configurations
DEFAULT_CHAINS: Final[dict[str, dict[str, str | int]]] = {
    "zkSync": {
        "rpc_url": "https://zksync-era.blockpi.network/v1/rpc/public",
        "chain_id": 324,
        "block_explorer_url": "https://explorer.zksync.io",
        "oracle_url": "https://b0ywfwgey8.execute-api.us-east-1.amazonaws.com/signed_prices/latest",
        "tokens_url": "https://b0ywfwgey8.execute-api.us-east-1.amazonaws.com/tokens",
        # https://explorer.zksync.io/address/0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91
        "weth_address": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
        # USDC.e bridged: https://explorer.zksync.io/address/0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4
        # USDC: https://explorer.zksync.io/address/0x7455eb101303877511d73c5841Fbb088801f9b12
        "usdc_address": "0x7455eb101303877511d73c5841Fbb088801f9b12",
    },
    "zkSyncSepolia": {
        "rpc_url": "https://sepolia.era.zksync.dev/rpc",
        "chain_id": 300,
        "block_explorer_url": "https://sepolia.explorer.zksync.io",
        "oracle_url": "https://k5npgabr92.execute-api.us-east-1.amazonaws.com/signed_prices/latest",
        "tokens_url": "https://k5npgabr92.execute-api.us-east-1.amazonaws.com/tokens",
        "weth_address": "",
        "usdc_address": "0xAe045DE5638162fa134807Cb558E15A3F5A7F853",
    },
    "Arbitrum": {
        "rpc_url": "https://arb1.arbitrum.io/rpc",
        "chain_id": 42161,
        "block_explorer_url": "https://arbiscan.io",
        "oracle_url": "https://arbitrum-api.gmxinfra.io/signed_prices/latest",
        "tokens_url": "https://arbitrum-api.gmxinfra.io/tokens",
        # WETH: https://arbiscan.io/address/0x82aF49447D8a07e3bd95BD0d56f35241523fBab1
        "weth_address": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        # Native USDC: https://arbiscan.io/address/0xaf88d065e77c8cC2239327C5EDb3A432268e5831
        # Bridged USDC.e: https://arbiscan.io/token/0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8 - no route/markets
        "usdc_address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    },
}

CONTRACT_MAP: Final[dict[str, dict[str, dict[str, str]]]] = {
    "Arbitrum": {
        "data_store": {
            "contract_address": "0xFD70de6b91282D8017aA4E741e9Ae325CAb992d8",
            "abi_path": "contracts/arbitrum/data_store.json",
        },
        "event_emitter": {
            "contract_address": "0xC8ee91A54287DB53897056e12D9819156D3822Fb",
            "abi_path": "contracts/arbitrum/event_emitter.json",
        },
        "exchange_router": {
            "contract_address": "0x69C527fC77291722b52649E45c838e41be8Bf5d5",
            "abi_path": "contracts/arbitrum/exchange_router.json",
        },
        "deposit_vault": {
            "contract_address": "0xF89e77e8Dc11691C9e8757e84aaFbCD8A67d7A55",
            "abi_path": "contracts/arbitrum/deposit_vault.json",
        },
        "withdrawal_vault": {
            "contract_address": "0x0628D46b5D145f183AdB6Ef1f2c97eD1C4701C55",
            "abi_path": "contracts/arbitrum/withdrawal_vault.json",
        },
        "order_vault": {
            "contract_address": "0x31eF83a530Fde1B38EE9A18093A333D8Bbbc40D5",
            "abi_path": "contracts/arbitrum/order_vault.json",
        },
        "synthetics_reader": {
            "contract_address": "0x5Ca84c34a381434786738735265b9f3FD814b824",
            "abi_path": "contracts/arbitrum/synthetics_reader.json",
        },
        "synthetics_router": {
            "contract_address": "0x7452c558d45f8afC8c83dAe62C3f8A5BE19c71f6",
            "abi_path": "contracts/arbitrum/synthetics_router.json",
        },
    },
    "Avalanche": {
        "data_store": {
            "contract_address": "0x2F0b22339414ADeD7D5F06f9D604c7fF5b2fe3f6",
            "abi_path": "contracts/avalanche/data_store.json",
        },
        "event_emitter": {
            "contract_address": "0xDb17B211c34240B014ab6d61d4A31FA0C0e20c26",
            "abi_path": "contracts/avalanche/event_emitter.json",
        },
        "exchange_router": {
            "contract_address": "0x3BE24AED1a4CcaDebF2956e02C27a00726D4327d",
            "abi_path": "contracts/avalanche/exchange_router.json",
        },
        "deposit_vault": {
            "contract_address": "0x90c670825d0C62ede1c5ee9571d6d9a17A722DFF",
            "abi_path": "contracts/avalanche/deposit_vault.json",
        },
        "withdrawal_vault": {
            "contract_address": "0xf5F30B10141E1F63FC11eD772931A8294a591996",
            "abi_path": "contracts/avalanche/withdrawal_vault.json",
        },
        "order_vault": {
            "contract_address": "0xD3D60D22d415aD43b7e64b510D86A30f19B1B12C",
            "abi_path": "contracts/avalanche/order_vault.json",
        },
        "synthetics_reader": {
            "contract_address": "0xBAD04dDcc5CC284A86493aFA75D2BEb970C72216",
            "abi_path": "contracts/avalanche/synthetics_reader.json",
        },
        "synthetics_router": {
            "contract_address": "0x820F5FfC5b525cD4d88Cd91aCf2c28F16530Cc68",
            "abi_path": "contracts/avalanche/synthetics_router.json",
        },
    },
    "zkSyncSepolia": {
        "data_store": {
            "contract_address": "0xD5a9c50e65eBcF20DF8Df7d3f0D825D8202EBEfc",
            "abi_path": "contracts/zksync_sepolia/data_store.json",
        },
        "event_emitter": {
            "contract_address": "0x2011E4372D681AEB2B62DBFe9806b0C6c963eE1c",
            "abi_path": "contracts/zksync_sepolia/event_emitter.json",
        },
        "exchange_router": {
            "contract_address": "0xa64a7FdD8ab84157172a781691380316010204A3",
            "abi_path": "contracts/zksync_sepolia/exchange_router.json",
        },
        "deposit_vault": {
            "contract_address": "0x1B8CB84caC7fbAb848670B331f49759C3c1d976f",
            "abi_path": "contracts/zksync_sepolia/deposit_vault.json",
        },
        "withdrawal_vault": {
            "contract_address": "0xC3A463123eF29Fab3b0935889ADd502B38CbB9aC",
            "abi_path": "contracts/zksync_sepolia/withdrawal_vault.json",
        },
        "order_vault": {
            "contract_address": "0x964163A7b0F4C0E36F6684786261B786Ae4090c4",
            "abi_path": "contracts/zksync_sepolia/order_vault.json",
        },
        "synthetics_reader": {
            "contract_address": "0xD9c04c3d2258438f8E38381E61e854f6dC8Caea2",
            "abi_path": "contracts/zksync_sepolia/synthetics_reader.json",
        },
        "synthetics_router": {
            "contract_address": "0x38f2543e8c6C6954E71fA1cAa2eb9d39fBE64107",
            "abi_path": "contracts/zksync_sepolia/synthetics_router.json",
        },
    },
    "zkSync": {
        "data_store": {
            "contract_address": "0x6E5E072e27368A68673E86f19Ed9C7C5C1dcBB7c",
            "abi_path": "contracts/zksync/data_store.json",
        },
        "event_emitter": {
            "contract_address": "0x84AF4e95e072422d5632aA24b857fd924ED0EB6a",
            "abi_path": "contracts/zksync/event_emitter.json",
        },
        "exchange_router": {
            "contract_address": "0xd68a502766fa96921820Ea465985405f69366837",
            "abi_path": "contracts/zksync/exchange_router.json",
        },
        "deposit_vault": {
            "contract_address": "0xD0eB16699C7B98967B9039503B23E28eC045F7F0",
            "abi_path": "contracts/zksync/deposit_vault.json",
        },
        "withdrawal_vault": {
            "contract_address": "0xBEb20009FeE5E71e3460B31d9dc26cd989a0DE03",
            "abi_path": "contracts/zksync/withdrawal_vault.json",
        },
        "order_vault": {
            "contract_address": "0x88dCff05CA4D0a65ac70768159517b2edE082B41",
            "abi_path": "contracts/zksync/order_vault.json",
        },
        "synthetics_reader": {
            "contract_address": "0x2F48EeDb50F6087E5C164731CD3DbdA8a4514b17",
            "abi_path": "contracts/zksync/synthetics_reader.json",
        },
        "synthetics_router": {
            "contract_address": "0x18f8773B66991CC8Af7C5E7adbfd59A62d0cAB2E",
            "abi_path": "contracts/zksync/synthetics_router.json",
        },
    },
}


class ConfigManager:
    """
    Manages configuration settings such as RPC URLs, wallet addresses, and chain information.
    """

    def __init__(
        self,
        chain: str = "zkSync",
        rpc_url: str | None = None,
        chain_id: int | None = None,
        block_explorer_url: str | None = None,
        oracle_url: str | None = None,
        tokens_url: str | None = None,
        user_wallet_address: ChecksumAddress | str | None = None,
        private_key: str | None = None,
        save_to_json: bool = False,
        save_to_csv: bool = False,
        output_data_folder: Path | str | None = None,
    ) -> None:
        """
        Initializes the ConfigManager with the given blockchain network configuration.

        :param chain: The blockchain network name (e.g., 'zkSync', 'Arbitrum').
        :param rpc_url: Optional RPC URL for interacting with the blockchain.
        :param chain_id: Optional chain ID for the blockchain network.
        :param block_explorer_url: Optional block explorer URL for the blockchain.
        :param oracle_url: Optional oracle URL for the blockchain.
        :param tokens_url: Optional tokens URL for the blockchain.
        :param user_wallet_address: Optional wallet address of the user.
        :param private_key: Optional private key associated with the wallet.
        :param save_to_json: Optional boolean flag indicating whether to save outputs to JSON.
        :param save_to_csv: Optional boolean flag indicating whether to save outputs to CSV.
        :param output_data_folder: Optional output data folder path.
        """
        self.chain: Final[str] = chain

        # Set defaults from known chains
        defaults: dict[str, str | int] = DEFAULT_CHAINS.get(chain)
        if not defaults:
            raise ValueError(f"No chain info was found for chain: {chain}")

        # Use a generic initializer method
        self.rpc_url: Final[str] = self._get_value(rpc_url, defaults, "rpc_url")
        self.chain_id: Final[int] = self._get_value(chain_id, defaults, "chain_id")
        self.block_explorer_url: Final[str] = self._get_value(block_explorer_url, defaults, "block_explorer_url")
        self.oracle_url: Final[str] = self._get_value(oracle_url, defaults, "oracle_url")
        self.tokens_url: Final[str] = self._get_value(tokens_url, defaults, "tokens_url")

        # Set up blockchain connection
        self.connection: Final[Web3] = Web3(Web3.HTTPProvider(self.rpc_url))
        self.contracts: Final[NetworkContracts] = self._initialize_chain_contracts()

        # Wallet and private key handling
        self.user_wallet_address: ChecksumAddress = self._initialize_wallet_address(user_wallet_address)
        self.private_key: str = self._initialize_private_key(private_key)

        # Storage flags and output data folder
        self.save_to_json: bool = save_to_json
        self.save_to_csv: bool = save_to_csv
        if output_data_folder:
            self.data_path: Path = (
                output_data_folder if isinstance(output_data_folder, Path) else Path(output_data_folder)
            )
        else:
            self.data_path = None
        if (self.save_to_json or self.save_to_csv) and self.data_path is None:
            logging.error("No data path was specified.")
            raise ValueError("No data path was specified.")

        # Set well-known addresses
        self.weth_address: ChecksumAddress = self.to_checksum_address(defaults.get("weth_address"))
        self.usdc_address: ChecksumAddress = self.to_checksum_address(defaults.get("usdc_address"))
        self.zero_address: ChecksumAddress = self.to_checksum_address("0x0000000000000000000000000000000000000000")

    @staticmethod
    def _get_value(provided_value: Any, defaults: dict[str, Any], key: str) -> Any:
        """
        Retrieve a value either from provided arguments or from defaults.

        :param provided_value: The value provided during initialization.
        :param defaults: A dictionary containing default chain configuration values.
        :param key: The key to look up in the defaults if the provided value is None.
        :return: The value for the given key, either provided or from defaults.
        :raises ValueError: If neither the provided value nor a default is available.
        """
        value: Any = provided_value or defaults.get(key)
        if value is None:
            logging.error(f"No value was specified for {key}.")
            raise ValueError(f"No value was specified for {key}.")
        return value

    def _initialize_chain_contracts(self) -> NetworkContracts:
        """
        Initializes the contract information for the selected chain, converting addresses to checksum format.

        :return: The initialized NetworkContracts object containing contract addresses and ABI paths.
        :raises ValueError: If no chain contracts are found for the specified chain.
        """
        chain_contracts: dict[str, dict[str, str]] | None = CONTRACT_MAP.get(self.chain)
        if not chain_contracts:
            logging.error(f"No chain contracts were found for chain: {self.chain}")
            raise ValueError(f"No chain contracts were found for chain: {self.chain}")

        return NetworkContracts(
            **{
                contract_name: ContractInfo(
                    contract_address=self.to_checksum_address(info["contract_address"]),
                    abi_path=info["abi_path"],
                )
                for contract_name, info in chain_contracts.items()
            }
        )

    def to_checksum_address(self, address: str) -> ChecksumAddress:
        """
        Converts an address to checksum format.

        :param address: The address to convert.
        :return: The checksummed address.
        """
        return self.connection.to_checksum_address(address)

    def _initialize_wallet_address(self, user_wallet_address: str | None) -> ChecksumAddress:
        """
        Initializes the user wallet address, either from the provided argument or environment variables.

        :param user_wallet_address: Optional user wallet address. If not provided, fetches from environment variables.
        :return: The checksummed wallet address.
        :raises ValueError: If no wallet address is provided or found in environment variables.
        """
        user_wallet_address: str = user_wallet_address or os.getenv("USER_WALLET_ADDRESS")
        if not user_wallet_address:
            logging.error("No user wallet address was specified.")
            raise ValueError("User wallet address not provided.")
        return self.to_checksum_address(user_wallet_address)

    @staticmethod
    def _initialize_private_key(private_key: str | None) -> str:
        """
        Initializes the private key, either from the provided argument or environment variables.

        :param private_key: The private key.
        :return: The initialized private key.
        :raises ValueError: If no private key is provided or found in environment variables.
        """
        private_key: str = private_key or os.getenv("PRIVATE_KEY")
        if not private_key:
            logging.error("No private key was specified.")
            raise ValueError("Private key not provided.")
        return private_key

    def __repr__(self) -> str:
        """
        Returns a string representation of the ConfigManager object, masking sensitive information.

        :return: A string representation of the ConfigManager.
        """
        return (
            f"ConfigManager(chain={self.chain}, "
            f"rpc_url={self.rpc_url}, "
            f"user_wallet_address={self.user_wallet_address}, "
            f"private_key={'<hidden>' if self.private_key else 'None'})"
        )
