import json
import logging
from logging import Logger
from pathlib import Path

from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
from web3.contract import Contract
from web3.types import ChecksumAddress, TxParams

from pyrfx.config_manager import ConfigManager


def check_if_approved(
    config: ConfigManager,
    spender_address: str | ChecksumAddress,
    token_to_approve_address: str | ChecksumAddress,
    amount_of_tokens_to_spend: int,
    max_fee_per_gas: int,
    approve: bool,
    logger: Logger | None = None,
) -> None:
    """
    Check if a given amount of tokens is approved for spending by a contract, and approve if necessary.

    :param config: The configuration object containing network and user details.
    :param spender_address: The contract address of the requested spender.
    :param token_to_approve_address: The contract address of the token to spend.
    :param amount_of_tokens_to_spend: The amount of tokens to spend, in expanded decimals.
    :param max_fee_per_gas: The maximum fee per gas to be used for the transaction.
    :param approve: Set to True if you want to approve spending if not already approved.
    :param logger: The logger object.

    :raises Exception: If there is an insufficient balance or the token is not approved for spending.
    :return: None.
    """
    if not logger:
        logger: Logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

    # Convert addresses to checksum format
    if not isinstance(spender_address, ChecksumAddress):
        spender_address: ChecksumAddress = config.to_checksum_address(address=spender_address)
    if not isinstance(token_to_approve_address, ChecksumAddress):
        token_to_approve_address: ChecksumAddress = config.to_checksum_address(address=token_to_approve_address)
    user_wallet_address: str | ChecksumAddress | None = config.user_wallet_address
    if not isinstance(user_wallet_address, ChecksumAddress):
        user_wallet_address: ChecksumAddress = config.to_checksum_address(address=user_wallet_address)

    # Load ABI for the token contract
    file_path: Path = Path(__file__).parent / "contracts" / "token_approval.json"

    # Check if the file exists before trying to open it
    if file_path.exists():
        with file_path.open() as file:
            token_contract_abi: dict = json.load(file)
    else:
        logger.error(f"The file {file_path} does not exist.")
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    token_contract_obj: Contract = config.connection.eth.contract(
        address=token_to_approve_address, abi=token_contract_abi
    )

    # Get user balance
    if token_to_approve_address == config.weth_address:
        # Balance of WETH
        balance_of: int = config.connection.eth.get_balance(user_wallet_address)
    else:
        # Balance of other token
        balance_of: int = token_contract_obj.functions.balanceOf(user_wallet_address).call()

    # Raise an exception if the user doesn't have enough tokens
    if balance_of < amount_of_tokens_to_spend:
        logger.error("Insufficient balance!")
        raise Exception("Insufficient balance!")

    # Check the amount already approved for the spender
    amount_approved: int = token_contract_obj.functions.allowance(user_wallet_address, spender_address).call()

    logger.info("Checking if tokens are already approved for spending...")

    # If the tokens are not approved and approval is requested, approve them
    if amount_approved < amount_of_tokens_to_spend and approve:
        logger.info(
            f'Approving contract "{spender_address}" to spend {amount_of_tokens_to_spend} '
            f"tokens belonging to token address: {token_to_approve_address}"
        )

        nonce: int = config.connection.eth.get_transaction_count(user_wallet_address)

        # Build the transaction to approve token spending
        raw_txn: TxParams = token_contract_obj.functions.approve(
            spender_address, amount_of_tokens_to_spend
        ).build_transaction(
            {
                "value": 0,
                "chainId": config.chain_id,
                "gas": 4000000,
                "maxFeePerGas": int(max_fee_per_gas),
                "maxPriorityFeePerGas": 0,
                "nonce": nonce,
            }
        )

        # Sign the transaction with the user's private key
        signed_txn: SignedTransaction = config.connection.eth.account.sign_transaction(raw_txn, config.private_key)
        tx_hash: HexBytes = config.connection.eth.send_raw_transaction(signed_txn.rawTransaction)

        tx_url: str = f"{config.block_explorer_url}/tx/{tx_hash.hex()}"
        logger.info(f"Transaction submitted! HEX: {tx_hash.hex()}")
        logger.info(f"Transaction submitted! Check status: {tx_url}")

    # If tokens are not approved but approval is not requested, raise an exception
    elif amount_approved < amount_of_tokens_to_spend and not approve:
        raise Exception("Token not approved for spend, please allow first!")

    # If tokens are already approved or successfully approved, print confirmation
    logger.info(
        f'Contract "{spender_address}" approved to spend {amount_of_tokens_to_spend} '
        f"tokens belonging to token address: {token_to_approve_address}"
    )
    logger.info("Tokens approved for spending!")


if __name__ == "__main__":
    # Initialize logging
    from pyrfx.logging_setup import logging_setup

    logging_setup()

    # Initialize config
    config: ConfigManager = ConfigManager(chain="arbitrum")
    logging.info(config)

    # Example parameters
    # Replace with actual spender contract address
    spender: str = "0xSpenderAddress"
    # Replace with actual token contract address
    token_to_approve: str = "0xTokenToApproveAddress"
    # Example amount in expanded decimals (e.g., 1 token with 18 decimals)
    amount_of_tokens_to_spend: int = 10**18
    # Example max fee per gas (1 gwei)
    max_fee_per_gas: int = 1000000000
    # Set to True if you want to approve the token spending
    approve: bool = True

    # Call the function to check if tokens are approved and approve if needed
    check_if_approved(
        config=config,
        spender_address=spender,
        token_to_approve_address=token_to_approve,
        amount_of_tokens_to_spend=amount_of_tokens_to_spend,
        max_fee_per_gas=max_fee_per_gas,
        approve=approve,
    )
