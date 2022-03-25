from __future__ import annotations
import dataclasses
import decimal
import typing
from cvm  import balances, datatypes
from icvm import collection, utils

@dataclasses.dataclass(init=True, frozen=True)
class Efficiency(collection.IndicatorCollection):
    gross_margin: decimal.Decimal
    """Margem Bruta"""

    ebitda_margin: typing.Optional[decimal.Decimal]
    """Margem EBITDA"""

    ebit_margin: decimal.Decimal
    """Margem EBIT"""

    net_margin: decimal.Decimal
    """Margem Líquida"""

    @classmethod
    def from_industrial(cls, dfpitr: datatypes.BalanceType, industrial: balances.IndustrialCollection) -> Efficiency:
        dre = industrial.dre

        return Efficiency(
            gross_margin  = utils.zero_safe_divide(dre.gross_profit, dre.net_revenue),
            ebitda_margin = utils.none_safe_divide(dre.ebitda,       dre.net_revenue),
            ebit_margin   = utils.zero_safe_divide(dre.ebit,         dre.net_revenue),
            net_margin    = utils.zero_safe_divide(dre.net_profit,   dre.net_revenue)
        )