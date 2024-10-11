from eth_account.signers.local import LocalAccount
from mach_client import Token

from .. import config
from ..log import LogContextAdapter, Logger
from ..transactions import approve_send_contract_function_transaction
from ..utility import make_w3, make_token_contract


async def supply(token: Token, account: LocalAccount, log: Logger) -> int:
    log = LogContextAdapter(log, f"{token} => Aave")

    w3 = await make_w3(token.chain)
    token_contract = make_token_contract(w3, token)

    if (
        balance := await token_contract.functions.balanceOf(account.address).call()
    ) <= 0:
        log.warning(f"Balance was empty, not supplying")
        return 0

    aave_pool_address = config.aave_pool_addresses[token.chain.id]
    pool_contract = w3.eth.contract(
        address=aave_pool_address, abi=config.aave_pool_abi(token.chain.id)  # type: ignore
    )
    supply_function = pool_contract.functions.supply(
        token.contract_address,
        balance,
        account.address,
        0,  # Referral code
    )

    log.info(f"Supplying {balance} units")

    await approve_send_contract_function_transaction(
        supply_function,
        account,
        token_contract,
        balance,
        log,
    )

    log.info(f"Supply successful")

    return balance
