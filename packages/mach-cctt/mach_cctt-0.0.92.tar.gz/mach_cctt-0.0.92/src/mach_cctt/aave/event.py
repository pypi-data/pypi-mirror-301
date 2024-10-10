from dataclasses import dataclass

from mach_client import Token


@dataclass
class ChoseNextToken:
    token: Token
    interest_rate: float


@dataclass
class Withdraw:
    amounts: list[tuple[Token, float]]


@dataclass
class Supply:
    token: Token
    amount: float


@dataclass
class ChooseTokenError:
    exception: Exception


@dataclass
class WithdrawError:
    token: Token
    exception: Exception


@dataclass
class ConvertError:
    src_token: Token
    dest_token: Token
    error: object


@dataclass
class SupplyError:
    token: Token
    amount: float
    exception: Exception


AaveError = ChooseTokenError | WithdrawError | ConvertError | SupplyError

AaveEvent = ChoseNextToken | Withdraw | Supply | AaveError
