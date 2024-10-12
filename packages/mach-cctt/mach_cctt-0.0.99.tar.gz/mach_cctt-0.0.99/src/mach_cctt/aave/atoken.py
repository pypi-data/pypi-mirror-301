from eth_typing import ChecksumAddress
from mach_client import ChainId, Token, config as client_config
from web3 import AsyncWeb3

from .. import config


async def get_all_atokens(w3: AsyncWeb3, chain: ChainId) -> dict[str, ChecksumAddress]:
    contract_address = config.aave_pool_data_provider_addresses[chain]
    pool_data_provider = w3.eth.contract(address=contract_address, abi=config.aave_pool_data_provider_abi)  # type: ignore

    # Tuples (symbol, address) where the symbol is of the form "a<first 3 letters of chain name><symbol name>", ie. aArbUSDC
    atokens: list[tuple[str, ChecksumAddress]] = (
        await pool_data_provider.functions.getAllATokens().call()
    )

    return {symbol[4:]: address for symbol, address in atokens}


# DIY cache since functools.cache doesn't work with async functions
atokens = {}


async def get_atoken_balance(
    w3: AsyncWeb3, token: Token, wallet: ChecksumAddress
) -> int:
    global atokens

    chain = token.chain.id

    if not atokens.get(chain, None):
        atokens[chain] = await get_all_atokens(w3, chain)

    token_address = atokens[chain][token.symbol]
    token_contract = w3.eth.contract(address=token_address, abi=client_config.erc20_abi)  # type: ignore
    balance = await token_contract.functions.balanceOf(wallet).call()

    # Aave has this weird thing with USDC where the atoken with symbol "USDC" actually represents a wrapped version
    # The "USDCn" token represents your actual USDC balance in the pool, where "n" stands for "native"
    if native_token_address := atokens[chain].get(f"{token.symbol}n"):
        native_token_contract = w3.eth.contract(
            address=native_token_address, abi=client_config.erc20_abi
        )
        balance += await native_token_contract.functions.balanceOf(wallet).call()

    return balance
