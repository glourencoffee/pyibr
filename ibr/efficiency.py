from __future__ import annotations
import cvm
import dataclasses
import decimal
import typing
from ibr.utils import zero_safe_divide, none_safe_divide

@dataclasses.dataclass(init=True)
class Efficiency:
    gross_margin: decimal.Decimal
    """Margem Bruta"""

    ebitda_margin: typing.Optional[decimal.Decimal]
    """Margem EBITDA"""

    ebit_margin: decimal.Decimal
    """Margem EBIT"""

    net_margin: decimal.Decimal
    """Margem Líquida"""

    @staticmethod
    def from_statement(income_statement: cvm.IncomeStatement) -> Efficiency:
        i = income_statement

        return Efficiency(
            gross_margin  = zero_safe_divide(i.gross_profit, i.revenue),
            ebitda_margin = none_safe_divide(i.ebitda,       i.revenue),
            ebit_margin   = zero_safe_divide(i.ebit,         i.revenue),
            net_margin    = zero_safe_divide(i.net_income,   i.revenue)
        )