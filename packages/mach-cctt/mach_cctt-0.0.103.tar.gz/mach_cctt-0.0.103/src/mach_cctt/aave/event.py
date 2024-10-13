from dataclasses import dataclass

from mach_client import Token


@dataclass
class FetchLiquidityRates:
    rates: list[tuple[Token, float]]


@dataclass
class Withdraw:
    amounts: list[tuple[Token, float]]


@dataclass
class Supply:
    amounts: list[tuple[Token, float]]

@dataclass
class LiquidityRateError:
    tokens: list[Token]
    exception: Exception


@dataclass
class WithdrawError:
    token: Token
    amount: float
    exception: Exception


@dataclass
class ConvertError:
    src_token: Token
    error: object


@dataclass
class SupplyError:
    token: Token
    amount: float
    exception: Exception


AaveError = LiquidityRateError | WithdrawError | ConvertError | SupplyError

AaveEvent = FetchLiquidityRates | Withdraw | Supply | AaveError
