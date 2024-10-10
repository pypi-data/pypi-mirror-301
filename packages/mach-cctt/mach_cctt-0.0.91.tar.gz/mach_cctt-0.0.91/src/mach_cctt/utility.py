from typing import AbstractSet, Optional

from eth_typing import ChecksumAddress
from mach_client import Chain, ChainId, Token, client
from web3 import AsyncWeb3
from web3.contract import AsyncContract
from web3.middleware import ExtraDataToPOAMiddleware

from . import config


async def make_w3(chain: Chain) -> AsyncWeb3:
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(chain.rpc_url))
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    assert await w3.is_connected()

    return w3


def make_token_contract(w3: AsyncWeb3, token: Token) -> AsyncContract:
    return w3.eth.contract(
        address=AsyncWeb3.to_checksum_address(token.contract_address),
        abi=config.erc20_abi,
    )


def make_order_book_contract(w3: AsyncWeb3, token: Token) -> AsyncContract:
    return w3.eth.contract(
        address=client.deployments[token.chain.id]["contracts"]["order_book"],
        abi=config.order_book_abi,
    )


async def choose_source_token(
    excluded_chains: AbstractSet[ChainId], wallet_address: ChecksumAddress
) -> Token:
    balances = await client.get_token_balances(wallet_address)

    token: Optional[tuple[int, ChainId, str]] = None

    # Choose the token with the greatest balance (regardless of denomination) that is not the gas token
    for chain, chain_balances in filter(
        lambda item: item[0] not in excluded_chains, balances.items()
    ):
        for symbol, balance in chain_balances.items():
            if client.gas_tokens.get(chain, None) != symbol and (
                not token or token[0] < balance
            ):
                token = (balance, chain, symbol)

    if not token:
        raise RuntimeError("No viable source tokens to choose from")

    return Token(token[1], token[2])
