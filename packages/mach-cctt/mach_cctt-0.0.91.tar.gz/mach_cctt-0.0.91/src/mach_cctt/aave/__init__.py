import asyncio
from pprint import pformat
from typing import AsyncGenerator, Iterable, NamedTuple, Optional

from eth_account.signers.local import LocalAccount
from mach_client import ChainId, Token, client

from .. import config
from ..destination_policy import FixedTokenSingleTradePolicy
from ..log import Logger
from .. import mach
from ..mach.event import EmptySourceBalance, Trade
from ..utility import make_w3
from .event import *
from .supply import supply
from . import valid_tokens
from .withdraw import withdraw


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

    assert highest_token
    return highest_token, highest_rate


async def run(account: LocalAccount, log: Logger) -> AsyncGenerator[AaveEvent, None]:
    chains = client.chains - frozenset((ChainId.AVALANCHE_C_CHAIN, ChainId.POLYGON))
    symbols = frozenset(("USDC", "USDT", "FRAX", "DAI"))
    tokens = await valid_tokens.get_valid_aave_tokens(chains, symbols)

    log.debug(f"Tokens:\n{pformat(tokens)}")

    current_chain: Optional[ChainId] = None

    while True:
        try:
            next_token, rate = await get_highest_liquidity_rate_token(
                filter(lambda token: token.chain.id != current_chain, tokens)
                if current_chain
                else tokens
            )
        except Exception as e:
            log.critical(
                "An exception was thrown while fetching the highest liquidity rate token"
            )
            log.exception(e)
            yield ChooseTokenError(e)
            continue

        yield ChoseNextToken(next_token, rate)

        current_chain = None

        log.info(f"Next token: {next_token} at interest rate of {100 * rate}%")

        log.info(f"Withdrawing funds from Aave")

        withdrawn = []

        for token in filter(lambda token: token.chain != next_token.chain, tokens):
            try:
                if (withdrawn_amount := await withdraw(token, account, log)) > 0:
                    withdrawn.append((token, withdrawn_amount / 10**token.decimals))

            except Exception as e:
                log.critical(
                    f"An exception was thrown while withdrawing {token} from Aave:"
                )
                log.exception(e)
                yield WithdrawError(token, e)
                continue

        yield Withdraw(withdrawn)

        log.info(f"Swapping funds in wallet to {next_token}")

        for token in filter(lambda token: token.chain != next_token.chain, tokens):
            runner = mach.run(
                token,
                FixedTokenSingleTradePolicy(next_token),
                account,
                log,
            )

            try:
                async for event in runner:
                    # Only 2 successful cases are expected: either the trade goes through, or we never had any of the source token in the first place
                    if isinstance(event, (Trade, EmptySourceBalance)):
                        break

                    log.error(
                        f"Unexpected event while swapping {token} to {next_token}:"
                    )
                    log.error(pformat(event))
                    yield ConvertError(token, next_token, event)

            except Exception as e:
                log.critical(
                    f"An exception was thrown while swapping {token} to {next_token}:"
                )
                log.exception(e)
                yield ConvertError(token, next_token, e)
                continue

        try:
            if (amount := await supply(next_token, account, log)) <= 0:
                continue

        except Exception as e:
            log.critical(
                f"An exception was thrown while supplying {next_token} to Aave:"
            )
            log.exception(e)
            yield SupplyError(next_token, amount / 10**next_token.decimals, e)
            continue

        yield Supply(next_token, amount / 10**next_token.decimals)

        current_chain = next_token.chain.id

        log.info("Sleeping...")
        await asyncio.sleep(config.max_polls * config.poll_timeout)
