from eth_account.signers.local import LocalAccount
from mach_client import Token

from .. import config
from ..log import LogContextAdapter, Logger
from ..transactions import send_contract_function_transaction
from ..utility import make_w3
from .atoken import get_atoken_balance


async def withdraw(token: Token, account: LocalAccount, log: Logger) -> int:
    log = LogContextAdapter(log, f"Aave {token} => account")
    w3 = await make_w3(token.chain)

    if (balance := await get_atoken_balance(w3, token, account)) <= 0:
        log.debug("Balance was empty, not withdrawing")
        return 0

    aave_pool_address = config.aave_pool_addresses[token.chain.id]
    pool_contract = w3.eth.contract(
        address=aave_pool_address, abi=config.aave_pool_abi(token.chain.id)  # type: ignore
    )
    withdraw_function = pool_contract.functions.withdraw(
        token.contract_address,
        config.solidity_uint_max, # Means withdraw everything
        account.address,
    )

    log.info(f"Withdrawing {balance} units")

    await send_contract_function_transaction(withdraw_function, account, log)

    log.info(f"Withdraw successful")

    return balance
