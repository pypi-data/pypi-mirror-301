import json
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from enum import Enum
from logging import Logger
from pathlib import Path
from typing import Any, Callable, Final

import pandas as pd
import requests
from eth_abi import encode
from eth_account import Account
from pandas import DataFrame
from ratelimit import limits, sleep_and_retry
from tenacity import retry, stop_after_attempt, wait_exponential
from web3 import Web3
from web3.contract import Contract
from web3.exceptions import ContractLogicError

from pyrfx.config_manager import ConfigManager

PRECISION: Final[int] = 30

# Set up logging
logging.basicConfig(level=logging.INFO)
logger: Logger = logging.getLogger(__name__)


# Enum for Order Types
class OrderTypes(Enum):
    MARKET_SWAP = 0
    LIMIT_SWAP = 1
    MARKET_INCREASE = 2
    LIMIT_INCREASE = 3
    MARKET_DECREASE = 4
    LIMIT_DECREASE = 5
    STOP_LOSS_DECREASE = 6
    LIQUIDATION = 7


# Enum for Decrease Position Swap Types
class DecreasePositionSwapTypes(Enum):
    NO_SWAP = 0
    SWAP_PNL_TOKEN_TO_COLLATERAL_TOKEN = 1
    SWAP_COLLATERAL_TOKEN_TO_PNL_TOKEN = 2


# Constants for rate limiting
CALLS_PER_SECOND: Final[int] = 5
ONE_SECOND: Final[int] = 1


# Combined retrier and rate limiter decorator
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
@sleep_and_retry
@limits(calls=CALLS_PER_SECOND, period=ONE_SECOND)
def execute_call(call) -> Any:
    """
    Executes a Web3 call with retry logic and rate limiting.

    :param call: Web3 call to be executed.
    :return: The result of the Web3 call.
    """
    result = call.call()
    logger.debug("Web3 call executed successfully.")
    return result


# Executes multiple Web3 calls concurrently using ThreadPoolExecutor
def execute_threading(function_calls: list) -> list:
    """
    Execute multiple Web3 function calls concurrently using ThreadPoolExecutor.

    :param function_calls: A list of Web3 function calls to execute.
    :return: A list of results from the executed Web3 calls.
    """
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(execute_call, function_calls))
    logger.info("All Web3 calls executed successfully.")
    return results


def load_contract_abi(abi_file_path: Path) -> list[dict[str, Any]]:
    """
    Load the ABI file from the specified path.

    :param abi_file_path: Path to the ABI JSON file.
    :return: Loaded ABI as a list of dictionaries.
    :raises FileNotFoundError: If the file doesn't exist.
    :raises json.JSONDecodeError: If the JSON content is invalid.
    """
    try:
        return json.loads(abi_file_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading ABI from {abi_file_path}: {e}")
        raise


def get_contract_object(config: ConfigManager, contract_name: str) -> Contract:
    """
    Retrieve and instantiate a Web3 contract object using the contract name and chain.

    :param config: Configuration manager containing blockchain settings.
    :param contract_name: Name of the contract.
    :return: A Web3 contract object.
    :raises ValueError: If the contract information or ABI file is missing or invalid.
    :raises FileNotFoundError: If the ABI file is not found.
    :raises json.JSONDecodeError: If the ABI file is not valid JSON.
    """
    try:
        # Retrieve contract information
        contract_info = config.contracts[contract_name]

        # Load contract ABI
        abi_file_path = Path(__file__).parent / contract_info.abi_path
        logger.info(f"Loading ABI file from {abi_file_path}")
        contract_abi = load_contract_abi(abi_file_path)

        # Instantiate and return the Web3 contract object
        contract = config.connection.eth.contract(address=contract_info.contract_address, abi=contract_abi)
        logger.info(f"Contract object for '{contract_name}' on chain '{config.chain}' created successfully.")
        return contract

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading ABI for contract '{contract_name}': {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while creating contract object '{contract_name}': {e}")
        raise


def get_token_balance_contract(config: ConfigManager, contract_address: str) -> Contract | None:
    """
    Retrieve the contract object required to query a user's token balance.

    :param config: Configuration object containing RPC and chain details.
    :param contract_address: The token contract address to query balance from.
    :return: Web3 contract object or None if an error occurs.
    """
    abi_file_path = Path(__file__).parent / "contracts" / "balance_abi.json"

    try:
        # Load contract ABI and instantiate the contract
        contract_abi = load_contract_abi(abi_file_path)
        checksum_address = config.to_checksum_address(contract_address)
        contract = config.connection.eth.contract(address=checksum_address, abi=contract_abi)
        logger.debug(f"Contract for token balance at address {checksum_address} successfully created.")
        return contract
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading ABI or creating contract for address '{contract_address}': {e}")
        return None


def get_available_tokens(config: ConfigManager) -> dict[str, dict[str, str | int | bool]]:
    """
    Query the RFX API to generate a dictionary of available tokens for the specified chain.

    :param config: Configuration object containing the chain information.
    :return: Dictionary of available tokens.
    """
    try:
        response = requests.get(config.tokens_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        token_infos = response.json().get("tokens", [])
        logger.debug(f"Successfully fetched available tokens for chain {config.chain}.")
        return {token_info["address"]: token_info for token_info in token_infos}
    except requests.RequestException as e:
        logger.error(f"Error fetching tokens from API for chain {config.chain}: {e}")
        return {}


def get_contract(config: ConfigManager, contract_name: str) -> Contract:
    """
    Retrieve a contract object for the specified contract name and chain.

    :param config: Configuration object containing blockchain settings.
    :param contract_name: Name of the contract to retrieve.
    :return: Web3 contract object for the specified contract.
    :raises ValueError: If the contract information or ABI file is missing or invalid.
    :raises FileNotFoundError: If the ABI file is not found.
    :raises json.JSONDecodeError: If the ABI file is not valid JSON.
    """
    return get_contract_object(config=config, contract_name=contract_name)


def get_synthetics_reader_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the synthetics reader contract object for the specified chain.

    :param config: Configuration object containing blockchain settings.
    :return: Web3 contract object for the synthetics reader.
    """
    return get_contract(config, "synthetics_reader")


def get_event_emitter_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the event emitter contract object for the specified chain.

    :param config: Configuration object containing blockchain settings.
    :return: Web3 contract object for the event emitter.
    """
    return get_contract(config, "event_emitter")


def get_data_store_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the data store contract object for the specified chain.

    :param config: Configuration object containing blockchain settings.
    :return: Web3 contract object for the data store.
    """
    return get_contract(config, "data_store")


def get_exchange_router_contract(config: ConfigManager) -> Contract:
    """
    Retrieve the exchange router contract object for the specified chain.

    :param config: Configuration object containing blockchain settings.
    :return: Web3 contract object for the exchange router.
    """
    return get_contract(config, "exchange_router")


def create_signer(config: ConfigManager) -> Account | None:
    """
    Create a signer for the given chain using the private key.

    :param config: Configuration object containing the private key and chain information.
    :return: Web3 account object initialized with the private key.
    :raises ValueError: If the private key is missing or invalid.
    """
    if not config.private_key:
        raise ValueError("Private key is missing in the configuration.")

    return config.connection.eth.account.from_key(config.private_key)


def create_hash(data_type_list: list[str], data_value_list: list) -> bytes:
    """
    Create a keccak hash using a list of data types and their corresponding values.

    :param data_type_list: List of data types as strings.
    :param data_value_list: List of values corresponding to the data types.
    :return: Encoded and hashed key in bytes.
    """
    return Web3.keccak(encode(data_type_list, data_value_list))


def create_hash_string(string: str) -> bytes:
    """
    Create a keccak hash for a given string.

    :param string: The string to hash.
    :return: Hashed string in bytes.
    """
    return create_hash(["string"], [string])


def get_execution_price_and_price_impact(
    config: ConfigManager, params: dict[str, Any], decimals: int
) -> dict[str, float]:
    """
    Get the execution price and price impact for a position.

    :param config: Configuration object.
    :param params: Dictionary of the position parameters.
    :param decimals: Number of decimals for the token being traded.
    :return: A dictionary containing the execution price and price impact.
    """
    reader_contract = get_synthetics_reader_contract(config)

    output = execute_contract_function(
        reader_contract.functions.getExecutionPrice,
        params.get("data_store_address"),
        params.get("market_key"),
        params.get("index_token_price"),
        params.get("position_size_in_usd"),
        params.get("position_size_in_tokens"),
        params.get("size_delta"),
        params.get("is_long"),
    )

    return {
        "execution_price": (output[2] / pow(10, 30 - decimals)) if output else 0.0,
        "price_impact_usd": (output[0] / pow(10, 30)) if output else 0.0,
    }


def execute_contract_function(contract_function: Callable[..., Any], *args: Any) -> Any | None:
    """
    Execute a contract function call and return the result or handle exceptions.

    :param contract_function: The contract function to call.
    :param args: Arguments to pass to the contract function.
    :return: The result of the contract function call or None if an error occurs.
    """
    try:
        return contract_function(*args).call()
    except (ContractLogicError, ValueError) as e:
        logger.error(f"Error executing contract function {repr(contract_function)} with arguments {repr(args)}: {e}")


def get_estimated_swap_output(config: ConfigManager, params: dict[str, Any]) -> dict[str, float]:
    """
    Get the estimated swap output amount and price impact for a given chain and swap parameters.

    :param config: Configuration object containing chain information.
    :param params: Dictionary of the swap parameters.
    :return: A dictionary with the estimated token output and price impact.
    """
    reader_contract = get_synthetics_reader_contract(config)
    output = execute_contract_function(
        reader_contract.functions.getSwapAmountOut,
        params.get("data_store_address"),
        params.get("market_addresses"),
        params.get("token_prices_tuple"),
        params.get("token_in"),
        params.get("token_amount_in"),
        params.get("ui_fee_receiver"),
    )

    if output is None:
        logger.error("Failed to get swap output.")
        return {"out_token_amount": 0.0, "price_impact_usd": 0.0}

    return {
        "out_token_amount": output[0],
        "price_impact_usd": output[1],
    }


def get_estimated_deposit_amount_out(config: ConfigManager, params: dict[str, Any]) -> Any | None:
    """
    Get the estimated deposit amount output for a given chain and deposit parameters.

    :param config: Configuration object containing chain information.
    :param params: Dictionary of the deposit parameters.
    :return: The output of the deposit amount calculation or None if an error occurs.
    """
    return execute_contract_function(
        get_synthetics_reader_contract(config).functions.getDepositAmountOut,
        params.get("data_store_address"),
        params.get("market_addresses"),
        params.get("token_prices_tuple"),
        params.get("long_token_amount"),
        params.get("short_token_amount"),
        params.get("ui_fee_receiver"),
    )


def get_estimated_withdrawal_amount_out(config: ConfigManager, params: dict[str, Any]) -> Any | None:
    """
    Get the estimated withdrawal amount output for a given chain and withdrawal parameters.

    :param config: Configuration object containing chain information.
    :param params: Dictionary of the withdrawal parameters.
    :return: The output of the withdrawal amount calculation or None if an error occurs.
    """
    return execute_contract_function(
        get_synthetics_reader_contract(config).functions.getWithdrawalAmountOut,
        params.get("data_store_address"),
        params.get("market_addresses"),
        params.get("token_prices_tuple"),
        params.get("gm_amount"),
        params.get("ui_fee_receiver"),
    )


def find_dictionary_by_key_value(outer_dict: dict[str, dict], key: str, value: str) -> dict[str, Any] | None:
    """
    Search for a dictionary by key-value pair within an outer dictionary.

    :param outer_dict: The outer dictionary to search.
    :param key: The key to search for.
    :param value: The value to match.
    :return: The dictionary containing the matching key-value pair, or None if not found.
    """
    result = next((inner_dict for inner_dict in outer_dict.values() if inner_dict.get(key) == value), None)
    if result:
        logging.debug(f"Found dictionary for key={key}, value={value}")
    else:
        logging.debug(f"No dictionary found for key={key}, value={value}")
    return result


def apply_factor(value: int, factor: int) -> int:
    """
    Apply a factor to a value.

    :param value: The base value.
    :param factor: The factor to apply.
    :return: The adjusted value.
    """
    # constant is faster than 10**30,
    divisor: int = 1_000_000_000_000_000_000_000_000_000_000
    return value * factor // divisor


def get_funding_factor_per_period(
    market_info: dict, is_long: bool, period_in_seconds: int, long_interest_usd: int, short_interest_usd: int
) -> float:
    """
    Calculate the funding factor for a given period in a market.

    :param market_info: Dictionary of market parameters returned from the reader contract.
    :param is_long: Boolean indicating the direction of the position (long or short).
    :param period_in_seconds: The period in seconds over which to calculate the funding factor.
    :param long_interest_usd: Long interest in expanded decimals.
    :param short_interest_usd: Short interest in expanded decimals.
    :return: The funding factor for the specified period.
    """
    funding_factor_per_second = market_info["funding_factor_per_second"] * 1e-28
    long_pays_shorts = market_info["is_long_pays_short"]

    is_larger_side = long_pays_shorts if is_long else not long_pays_shorts

    if is_larger_side:
        return -funding_factor_per_second * period_in_seconds

    larger_interest_usd = long_interest_usd if long_pays_shorts else short_interest_usd
    smaller_interest_usd = short_interest_usd if long_pays_shorts else long_interest_usd

    ratio = (larger_interest_usd * pow(10, 30)) / smaller_interest_usd if smaller_interest_usd > 0 else 0
    return apply_factor(ratio, funding_factor_per_second) * period_in_seconds


def save_json(output_data_path: Path, file_name: str, data: dict) -> None:
    """
    Save a dictionary as a JSON file in the specified directory.

    :param output_data_path: The output data path.
    :param file_name: Name of the JSON file.
    :param data: Dictionary data to save.
    """
    output_data_path.mkdir(parents=True, exist_ok=True)
    file_path = output_data_path / file_name

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    logging.debug(f"Data saved to: {file_path}")


def save_csv(output_data_path: Path, file_name: str, data: DataFrame) -> None:
    """
    Save a Pandas DataFrame as a CSV file in the specified directory.

    :param output_data_path: The output data path.
    :param file_name: Name of the CSV file.
    :param data: Pandas DataFrame to save.
    """
    output_data_path.mkdir(parents=True, exist_ok=True)
    file_path = output_data_path / file_name

    # Append to existing file if it exists
    if file_path.exists():
        existing_data = pd.read_csv(file_path)
        data = pd.concat([existing_data, data], ignore_index=True)

    data.to_csv(file_path, index=False)
    logging.debug(f"Dataframe saved to: {file_path}")


def timestamp_df(data: dict) -> DataFrame:
    """
    Convert a dictionary into a Pandas DataFrame with a timestamp column.

    :param data: Dictionary data to convert.
    :return: DataFrame with timestamp column added.
    """
    data["timestamp"] = datetime.utcnow()
    return DataFrame([data])


def determine_swap_route(
    config: ConfigManager, markets: dict[str, dict], in_token: str, out_token: str
) -> tuple[list[str], bool]:
    """
    Find the list of RFX markets required to swap from one token to another.

    :param config: ConfigManager object containing chain configuration.
    :param markets: Dictionary of available markets.
    :param in_token: Contract address of the input token.
    :param out_token: Contract address of the output token.
    :return: A tuple containing the list of RFX markets and a boolean indicating if multi-swap is required.
    """
    if in_token == out_token:
        logging.info(f"Input token and output token are the same: {in_token}")
        return [], False

    # Handle case where input token is USDC
    if in_token == config.usdc_address:
        rfx_market = find_dictionary_by_key_value(markets, "index_token_address", out_token)
        if rfx_market:
            logging.info(f"Direct swap found from USDC to {out_token}")
            return [rfx_market["rfx_market_address"]], False
        else:
            logging.error(f"No direct market found for USDC to {out_token}")
            return [], False

    # Handle case where output token is USDC
    if out_token == config.usdc_address:
        rfx_market = find_dictionary_by_key_value(markets, "index_token_address", in_token)
        if rfx_market:
            logging.info(f"Direct swap found from {in_token} to USDC")
            return [rfx_market["rfx_market_address"]], False
        else:
            logging.error(f"No direct market found for {in_token} to USDC")
            return [], False

    # Attempt to find a two-step swap route (A -> B -> C)
    for market in markets.values():
        if market.get("index_token_address") == in_token:
            intermediate_token = market.get("paired_token_address")
            intermediate_market_address = market.get("rfx_market_address")

            if intermediate_token and intermediate_market_address:
                final_market = find_dictionary_by_key_value(markets, "index_token_address", out_token)
                if final_market and final_market.get("paired_token_address") == intermediate_token:
                    logging.info(f"Two-step swap route found from {in_token} to {out_token} via {intermediate_token}")
                    return [intermediate_market_address, final_market["rfx_market_address"]], True

    # If no route is found, log an error and return an empty path
    logging.error(f"No market found for swap from {in_token} to {out_token}")
    return [], False
