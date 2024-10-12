import asyncio
from pprint import pformat
from typing import AsyncGenerator, Optional, Sequence

from eth_account.signers.local import LocalAccount
from mach_client import ChainId, Token, client, utility

from .. import config
from ..destination_policy import FixedTokenSingleTradePolicy
from ..log import Logger
from .. import mach
from ..mach.event import EmptySourceBalance, Trade
from .event import *
from .supply import supply
from . import valid_tokens
from .withdraw import withdraw


scaling_factor = 10**27


async def get_liquidity_rate(token: Token) -> float:
    asset_info = client.deployments[token.chain.id]["assets"][token.symbol]

    w3 = await utility.make_w3(token.chain)

    aave_pool_address = config.aave_pool_addresses[token.chain.id]
    pool_contract = w3.eth.contract(
        address=aave_pool_address, abi=config.aave_pool_abi(token.chain.id)  # type: ignore
    )

    reserve_data = await pool_contract.functions.getReserveData(
        asset_info["address"]
    ).call()

    return reserve_data[2] / scaling_factor


async def get_highest_liquidity_rate_token(
    tokens: Sequence[Token],
) -> tuple[Token, float]:
    liquidity_rates = await asyncio.gather(
        *(get_liquidity_rate(token) for token in tokens)
    )

    idx, highest_rate = max(enumerate(liquidity_rates), key=lambda x: x[1])
    return tokens[idx], highest_rate


async def run(
    *,
    account: LocalAccount,
    logger: Logger,
) -> AsyncGenerator[AaveEvent, None]:
    chains = client.chains - frozenset(
        (ChainId.AVALANCHE_C_CHAIN, ChainId.BSC, ChainId.POLYGON)
    )
    symbols = frozenset(("USDC", "USDT", "FRAX", "DAI"))
    tokens = await valid_tokens.get_valid_aave_tokens(chains, symbols)

    logger.debug(f"Tokens:\n{pformat(tokens)}")

    current_chain: Optional[ChainId] = None

    while True:
        try:
            next_token, rate = await get_highest_liquidity_rate_token(
                tuple(filter(lambda token: token.chain.id != current_chain, tokens))
                if current_chain
                else tokens
            )
        except Exception as e:
            logger.critical(
                "An exception was thrown while fetching the highest liquidity rate token"
            )
            logger.exception(e)
            yield ChooseTokenError(e)
            continue

        current_chain = next_token.chain.id
        logger.info(f"Next token: {next_token} at interest rate of {100 * rate}%")

        yield ChoseNextToken(next_token, rate)

        logger.info(f"Withdrawing funds from Aave")

        withdrawn = []

        for token in filter(lambda token: token.chain != next_token.chain, tokens):
            amount, exception = await withdraw(token, account, logger)

            if exception:
                logger.critical(
                    f"An exception was thrown while withdrawing {token} from Aave:"
                )
                logger.exception(exception)
                yield WithdrawError(token, amount, exception)
                continue

            if amount > 0:
                withdrawn.append((token, amount / 10**token.decimals))

        yield Withdraw(withdrawn)

        logger.info(f"Swapping funds in wallet to {next_token}")

        for token in filter(lambda token: token.chain != next_token.chain, tokens):
            runner = mach.run(
                src_token=token,
                destination_policy=FixedTokenSingleTradePolicy(next_token),
                account=account,
                logger=logger,
            )

            try:
                async for event in runner:
                    # Only 2 successful cases are expected: either the trade goes through, or we never had any of the source token in the first place
                    if isinstance(event, (Trade, EmptySourceBalance)):
                        break

                    logger.error(
                        f"Unexpected event while swapping {token} to {next_token}:"
                    )
                    logger.error(pformat(event))
                    yield ConvertError(token, next_token, event)

            except Exception as e:
                logger.critical(
                    f"An exception was thrown while swapping {token} to {next_token}:"
                )
                logger.exception(e)
                yield ConvertError(token, next_token, e)

        amount, exception = await supply(next_token, account, logger)

        if exception:
            logger.critical(
                f"An exception was thrown while supplying {next_token} to Aave:"
            )
            logger.exception(exception)
            yield SupplyError(next_token, amount / 10**next_token.decimals, e)
            continue

        if amount <= 0:
            logger.warning("No funds to supply to Aave")
            continue

        yield Supply(next_token, amount / 10**next_token.decimals)

        logger.info("Sleeping...")
        await asyncio.sleep(config.max_polls * config.poll_timeout)
