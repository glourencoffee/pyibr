from __future__ import annotations
import dataclasses
import decimal
from cvm  import balances, datatypes
from icvm import collection, utils

@dataclasses.dataclass(init=True, frozen=True)
class Profitability(collection.IndicatorCollection):
    roe: decimal.Decimal
    """Return on Equity."""

    roa: decimal.Decimal
    """Return on Assets."""

    roic: decimal.Decimal
    """Return on Invested Capital."""

    asset_turnover: decimal.Decimal
    """'Giro de Ativo'"""

    @classmethod
    def from_industrial(cls, dfpitr: datatypes.BalanceType, industrial: balances.IndustrialCollection) -> Profitability:
        bpa = industrial.bpa
        bpp = industrial.bpp
        dre = industrial.dre

        gross_debt = bpp.current_loans_and_financing + bpp.noncurrent_loans_and_financing

        return Profitability(
            roe            = utils.zero_safe_divide(dre.net_profit,              bpp.net_equity),
            roa            = utils.zero_safe_divide(dre.net_profit,              bpa.total_assets),
            roic           = utils.zero_safe_divide(dre.ebit - dre.tax_expenses, bpp.net_equity + gross_debt),
            asset_turnover = utils.zero_safe_divide(dre.net_revenue,             bpa.total_assets)
        )