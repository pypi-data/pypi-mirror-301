from pyrfx.utils import create_hash, create_hash_string

# Precomputed hash strings for various keys (type: bytes)
ACCOUNT_POSITION_LIST: bytes = create_hash_string("ACCOUNT_POSITION_LIST")
CLAIMABLE_FEE_AMOUNT: bytes = create_hash_string("CLAIMABLE_FEE_AMOUNT")
DECREASE_ORDER_GAS_LIMIT: bytes = create_hash_string("DECREASE_ORDER_GAS_LIMIT")
DEPOSIT_GAS_LIMIT: bytes = create_hash_string("DEPOSIT_GAS_LIMIT")
WITHDRAWAL_GAS_LIMIT: bytes = create_hash_string("WITHDRAWAL_GAS_LIMIT")
EXECUTION_GAS_FEE_BASE_AMOUNT: bytes = create_hash_string("EXECUTION_GAS_FEE_BASE_AMOUNT")
EXECUTION_GAS_FEE_MULTIPLIER_FACTOR: bytes = create_hash_string("EXECUTION_GAS_FEE_MULTIPLIER_FACTOR")
INCREASE_ORDER_GAS_LIMIT: bytes = create_hash_string("INCREASE_ORDER_GAS_LIMIT")
MAX_OPEN_INTEREST: bytes = create_hash_string("MAX_OPEN_INTEREST")
MAX_POSITION_IMPACT_FACTOR_FOR_LIQUIDATIONS_KEY: bytes = create_hash_string(
    "MAX_POSITION_IMPACT_FACTOR_FOR_LIQUIDATIONS"
)
MAX_PNL_FACTOR_FOR_TRADERS: bytes = create_hash_string("MAX_PNL_FACTOR_FOR_TRADERS")
MAX_PNL_FACTOR_FOR_DEPOSITS: bytes = create_hash_string("MAX_PNL_FACTOR_FOR_DEPOSITS")
MAX_PNL_FACTOR_FOR_WITHDRAWALS: bytes = create_hash_string("MAX_PNL_FACTOR_FOR_WITHDRAWALS")
MIN_ADDITIONAL_GAS_FOR_EXECUTION: bytes = create_hash_string("MIN_ADDITIONAL_GAS_FOR_EXECUTION")
MIN_COLLATERAL_USD: bytes = create_hash_string("MIN_COLLATERAL_USD")
MIN_COLLATERAL_FACTOR_KEY: bytes = create_hash_string("MIN_COLLATERAL_FACTOR")
MIN_POSITION_SIZE_USD: bytes = create_hash_string("MIN_POSITION_SIZE_USD")
OPEN_INTEREST_IN_TOKENS: bytes = create_hash_string("OPEN_INTEREST_IN_TOKENS")
OPEN_INTEREST: bytes = create_hash_string("OPEN_INTEREST")
OPEN_INTEREST_RESERVE_FACTOR: bytes = create_hash_string("OPEN_INTEREST_RESERVE_FACTOR")
POOL_AMOUNT: bytes = create_hash_string("POOL_AMOUNT")
RESERVE_FACTOR: bytes = create_hash_string("RESERVE_FACTOR")
SINGLE_SWAP_GAS_LIMIT: bytes = create_hash_string("SINGLE_SWAP_GAS_LIMIT")
SWAP_ORDER_GAS_LIMIT: bytes = create_hash_string("SWAP_ORDER_GAS_LIMIT")
VIRTUAL_TOKEN_ID: bytes = create_hash_string("VIRTUAL_TOKEN_ID")


def account_position_list_key(account: str) -> bytes:
    """
    Generate a hash key for the account position list.

    :param account: The account address.
    :return: The hashed key for the account position list.
    """
    return create_hash(["bytes32", "address"], [ACCOUNT_POSITION_LIST, account])


def claimable_fee_amount_key(market: str, token: str) -> bytes:
    """
    Generate a hash key for claimable fee amount.

    :param market: The market address.
    :param token: The token address.
    :return: The hashed key for the claimable fee amount.
    """
    return create_hash(["bytes32", "address", "address"], [CLAIMABLE_FEE_AMOUNT, market, token])


def decrease_order_gas_limit_key() -> bytes:
    """
    Get the decrease order gas limit key.

    :return: The precomputed decrease order gas limit.
    """
    return DECREASE_ORDER_GAS_LIMIT


def deposit_gas_limit_key() -> bytes:
    """
    Get the deposit gas limit key.

    :return: The precomputed deposit gas limit.
    """
    return DEPOSIT_GAS_LIMIT


def execution_gas_fee_base_amount_key() -> bytes:
    """
    Get the execution gas fee base amount key.

    :return: The precomputed execution gas fee base amount.
    """
    return EXECUTION_GAS_FEE_BASE_AMOUNT


def execution_gas_fee_multiplier_key() -> bytes:
    """
    Get the execution gas fee multiplier factor key.

    :return: The precomputed execution gas fee multiplier factor.
    """
    return EXECUTION_GAS_FEE_MULTIPLIER_FACTOR


def increase_order_gas_limit_key() -> bytes:
    """
    Get the increase order gas limit key.

    :return: The precomputed increase order gas limit.
    """
    return INCREASE_ORDER_GAS_LIMIT


def min_additional_gas_for_execution_key() -> bytes:
    """
    Get the minimum additional gas for execution key.

    :return: The precomputed minimum additional gas for execution.
    """
    return MIN_ADDITIONAL_GAS_FOR_EXECUTION


def min_collateral() -> bytes:
    """
    Get the minimum collateral USD key.

    :return: The precomputed minimum collateral in USD.
    """
    return MIN_COLLATERAL_USD


def min_collateral_factor_key(market: str) -> bytes:
    """
    Generate a hash key for the minimum collateral factor for a market.

    :param market: The market address.
    :return: The hashed key for the minimum collateral factor.
    """
    return create_hash(["bytes32", "address"], [MIN_COLLATERAL_FACTOR_KEY, market])


def max_open_interest_key(market: str, is_long: bool) -> bytes:
    """
    Generate a hash key for the maximum open interest in a market.

    :param market: The market address.
    :param is_long: Boolean indicating long or short position.
    :return: The hashed key for maximum open interest.
    """
    return create_hash(["bytes32", "address", "bool"], [MAX_OPEN_INTEREST, market, is_long])


def max_position_impact_factor_for_liquidations_key(market: str) -> bytes:
    """
    Generate a hash key for the maximum position impact factor for liquidations in a market.

    :param market: The market address.
    :return: The hashed key for the maximum position impact factor for liquidations.
    """
    return create_hash(["bytes32", "address"], [MAX_POSITION_IMPACT_FACTOR_FOR_LIQUIDATIONS_KEY, market])


def open_interest_in_tokens_key(market: str, collateral_token: str, is_long: bool) -> bytes:
    """
    Generate a hash key for open interest in tokens.

    :param market: The market address.
    :param collateral_token: The collateral token address.
    :param is_long: Boolean indicating long or short position.
    :return: The hashed key for open interest in tokens.
    """
    return create_hash(
        ["bytes32", "address", "address", "bool"], [OPEN_INTEREST_IN_TOKENS, market, collateral_token, is_long]
    )


def open_interest_key(market: str, collateral_token: str, is_long: bool) -> bytes:
    """
    Generate a hash key for open interest.

    :param market: The market address.
    :param collateral_token: The collateral token address.
    :param is_long: Boolean indicating long or short position.
    :return: The hashed key for open interest.
    """
    return create_hash(["bytes32", "address", "address", "bool"], [OPEN_INTEREST, market, collateral_token, is_long])


def open_interest_reserve_factor_key(market: str, is_long: bool) -> bytes:
    """
    Generate a hash key for the open interest reserve factor in a market.

    :param market: The market address.
    :param is_long: Boolean indicating long or short position.
    :return: The hashed key for open interest reserve factor.
    """
    return create_hash(["bytes32", "address", "bool"], [OPEN_INTEREST_RESERVE_FACTOR, market, is_long])


def pool_amount_key(market: str, token: str) -> bytes:
    """
    Generate a hash key for the pool amount in a market.

    :param market: The market address.
    :param token: The token address.
    :return: The hashed key for the pool amount.
    """
    return create_hash(["bytes32", "address", "address"], [POOL_AMOUNT, market, token])


def reserve_factor_key(market: str, is_long: bool) -> bytes:
    """
    Generate a hash key for the reserve factor in a market.

    :param market: The market address.
    :param is_long: Boolean indicating long or short position.
    :return: The hashed key for reserve factor.
    """
    return create_hash(["bytes32", "address", "bool"], [RESERVE_FACTOR, market, is_long])


def single_swap_gas_limit_key() -> bytes:
    """
    Get the single swap gas limit key.

    :return: The precomputed single swap gas limit.
    """
    return SINGLE_SWAP_GAS_LIMIT


def swap_order_gas_limit_key() -> bytes:
    """
    Get the swap order gas limit key.

    :return: The precomputed swap order gas limit.
    """
    return SWAP_ORDER_GAS_LIMIT


def virtual_token_id_key(token: str) -> bytes:
    """
    Generate a hash key for the virtual token ID.

    :param token: The token address.
    :return: The hashed key for virtual token ID.
    """
    return create_hash(["bytes32", "address"], [VIRTUAL_TOKEN_ID, token])


def withdraw_gas_limit_key() -> bytes:
    """
    Get the withdrawal gas limit key.

    :return: The precomputed withdrawal gas limit.
    """
    return WITHDRAWAL_GAS_LIMIT
