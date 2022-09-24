from __future__ import annotations
import cvm
import dataclasses
import decimal
from ibr.utils import zero_safe_divide, none_safe_divide

@dataclasses.dataclass(init=True)
class Profitability:
    roe: decimal.Decimal
    """Return on Equity."""

    roa: decimal.Decimal
    """Return on Assets."""

    roic: decimal.Decimal
    """Return on Invested Capital."""

    asset_turnover: decimal.Decimal
    """'Giro de Ativo'"""

    @staticmethod
    def from_statement(balance_sheet: cvm.BalanceSheet, income_statement: cvm.IncomeStatement) -> Profitability:
        b = balance_sheet
        i = income_statement

        if b.gross_debt is None:
            equity_plus_gross_debt = None
        else:
            equity_plus_gross_debt = b.equity + b.gross_debt

        return Profitability(
            roe            = zero_safe_divide(i.net_income,            b.equity),
            roa            = zero_safe_divide(i.net_income,            b.total_assets),
            roic           = none_safe_divide(i.ebit - i.tax_expenses, equity_plus_gross_debt),
            asset_turnover = zero_safe_divide(i.revenue,               b.total_assets)
        )