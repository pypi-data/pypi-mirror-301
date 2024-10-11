import asyncio
import logging
from pprint import pformat
from typing import Iterable, NamedTuple, Optional

from eth_account.signers.local import LocalAccount
from mach_client import ChainId, Token, client

from .. import config
from ..destination_policy import FixedTokenSingleTradePolicy
from .. import mach
from ..utility import make_w3
from . import atoken, valid_tokens
from .supply import supply
from .withdraw import withdraw


logger = logging.getLogger("cctt")


class AaveMarketData(NamedTuple):
    liquidity_rate: float
    variable_borrow_rate: float
    stable_borrow_rate: float


scaling_factor = 10**27


async def get_market_data(pool_contract, asset_address) -> AaveMarketData:
    reserve_data = await pool_contract.functions.getReserveData(asset_address).call()
    return AaveMarketData(
        liquidity_rate=reserve_data[2] / scaling_factor,
        variable_borrow_rate=reserve_data[4] / scaling_factor,
        stable_borrow_rate=reserve_data[5] / scaling_factor,
    )


async def get_highest_liquidity_rate_token(
    tokens: Iterable[Token],
) -> tuple[Token, float]:
    highest_rate = -float("inf")
    highest_token: Optional[Token] = None

    for token in tokens:
        asset_info = client.deployments[token.chain.id]["assets"][token.symbol]

        w3 = await make_w3(token.chain)

        aave_pool_address = config.aave_pool_addresses[token.chain.id]
        pool_contract = w3.eth.contract(
            address=aave_pool_address, abi=config.aave_pool_abi(token.chain.id)  # type: ignore
        )

        market_data = await get_market_data(pool_contract, asset_info["address"])

        if market_data.liquidity_rate > highest_rate:
            highest_rate = market_data.liquidity_rate
            highest_token = token

    return highest_token, highest_rate  # type: ignore


async def run(account: LocalAccount) -> None:
    chains = client.chains - frozenset((ChainId.AVALANCHE_C_CHAIN, ChainId.POLYGON))
    symbols = frozenset(("USDC", "USDT", "FRAX", "DAI"))
    tokens = await valid_tokens.get_valid_aave_tokens(chains, symbols)

    logger.debug(f"Tokens:\n{pformat(tokens)}")

    current_chain: Optional[ChainId] = None

    while True:
        try:
            next_token, rate = await get_highest_liquidity_rate_token(
                filter(lambda token: token.chain.id != current_chain, tokens)
                if current_chain
                else tokens
            )

            logger.info(f"Next token: {next_token} at interest rate of {100 * rate}%")

            # TODO: async code breaks things so is commented out

            logger.info(f"Withdrawing funds from Aave")

            # await asyncio.gather(
            #     *map(
            #         lambda token: withdraw(token, account),
            #         # TODO: Mach can't handle single chain trades
            #         filter(lambda token: token.chain != next_token.chain, tokens),
            #     )
            # )

            for token in filter(lambda token: token.chain != next_token.chain, tokens):
                await withdraw(token, account)

            logger.info(f"Swapping funds in wallet to {next_token}")

            # Trick:
            #   - Run the Mach tester, but force it to make just a single swap to next token
            #   - Avoids having to write code dedicated to swapping token -> next_token

            # await asyncio.gather(
            #     *map(
            #         lambda token: mach_test.run(
            #             token, FixedTokenSingleTradePolicy(next_token), account
            #         ),
            #         filter(lambda token: token.chain != next_token.chain, tokens),
            #     )
            # )

            for token in filter(lambda token: token.chain != next_token.chain, tokens):
                runner = mach.run(
                    token, FixedTokenSingleTradePolicy(next_token), account, logger
                )

                async for _ in runner:
                    pass

            current_chain = next_token.chain.id

            if not await supply(next_token, account):
                continue

        except Exception as e:
            logger.warning(f"An exception was thrown during the test:")
            logger.exception(e)
            current_chain = None

        logger.info("Sleeping...")
        await asyncio.sleep(config.max_polls * config.poll_timeout)
