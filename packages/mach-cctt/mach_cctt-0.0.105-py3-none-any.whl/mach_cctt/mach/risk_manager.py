from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from eth_typing import ChecksumAddress
from mach_client import Quote, Token

from ..log import LogContextAdapter, Logger


@dataclass(kw_only=True)
class RiskAnalysis:
    reject: bool


class RiskManager(ABC):
    def __init__(self, wallet: ChecksumAddress, log: Logger):
        self.log = log
        self.wallet = wallet
        pass

    @abstractmethod
    def check_order(
        self, src_token: Token, dest_token: Token, quote: Quote
    ) -> RiskAnalysis:
        pass


# Reject high-slippage orders between "similar" tokens (ie. between USD stablecoins, wrapped ETH tokens, etc.)
class SimilarTokenRiskManager(RiskManager):
    @dataclass(kw_only=True)
    class RiskAnalysis(RiskAnalysis):
        slippage: Optional[float]
        slippage_tolerance: float

    special_usd_stablecoins = frozenset(
        (
            "DAI",
            "FRAX",
            "MIM",
        )
    )

    def __init__(self, wallet: ChecksumAddress, slippage_tolerance: float, log: Logger):
        assert -1.0 <= slippage_tolerance <= 0.0
        super().__init__(wallet, LogContextAdapter(log, "Slippage Manager"))
        self.slippage_tolerance = slippage_tolerance

    def is_usd_stablecoin(self, token: Token) -> bool:
        return "USD" in token.symbol or token.symbol in self.special_usd_stablecoins

    def check_order(
        self, src_token: Token, dest_token: Token, quote: Quote
    ) -> RiskAnalysis:
        if (
            src_token.symbol == dest_token.symbol
            or (src_token.is_usd_stablecoin() and dest_token.is_usd_stablecoin())
            or (src_token.is_eth() and dest_token.is_eth())
            or (src_token.is_btc() and dest_token.is_btc())
            or (src_token.is_eur_stablecoin() and dest_token.is_eur_stablecoin())
            or (src_token.is_gbp_stablecoin() and dest_token.is_gbp_stablecoin())
            or (src_token.is_jpy_stablecoin() and dest_token.is_jpy_stablecoin())
            or (src_token.is_chf_stablecoin() and dest_token.is_chf_stablecoin())
        ):
            # Convert from ticks to coin-denominated amounts
            src_amount = quote["src_amount"] / 10**src_token.decimals
            dest_amount = quote["dst_amount"] / 10**dest_token.decimals

            slippage = dest_amount / src_amount - 1.0
            self.log.info(f"{src_token} => {
                          dest_token} slippage: {100 * slippage}%")

            return self.RiskAnalysis(
                reject=slippage < self.slippage_tolerance,
                slippage=slippage,
                slippage_tolerance=self.slippage_tolerance,
            )

        # Always accept orders between dissimilar tokens
        self.log.info(f"{src_token} and {
                      dest_token} are not similar, ignoring")

        return self.RiskAnalysis(
            reject=False,
            slippage=None,
            slippage_tolerance=self.slippage_tolerance,
        )
