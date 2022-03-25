from __future__ import annotations
import dataclasses
import decimal
import typing
from cvm  import balances, datatypes
from icvm import collection, utils

@dataclasses.dataclass(init=True, frozen=True)
class Indebtedness(collection.IndicatorCollection):
    general_debt: decimal.Decimal
    """'Dívida Geral'"""

    debt_composition: decimal.Decimal
    """'Composição da Dívida' (CD)"""

    net_debt_over_net_equity: decimal.Decimal
    """'Dívida Líquida/Patrimônio Líquido'"""
    
    net_debt_over_ebitda: typing.Optional[decimal.Decimal]
    """'Dívida Líquida/EBITDA'"""
    
    net_debt_over_ebit: decimal.Decimal
    """'Dívida Líquida/EBIT'"""

    net_equity_over_assets: decimal.Decimal
    """'Dívida Líquida/Ativo'"""
    
    cassets_over_cliabilities: decimal.Decimal
    """'Ativo/Passivo'"""

    @classmethod
    def from_industrial(cls, dfpitr: datatypes.BalanceType, industrial: balances.IndustrialCollection) -> Indebtedness:
        bpa = industrial.bpa
        bpp = industrial.bpp
        dre = industrial.dre

        gross_debt = abs(bpp.current_loans_and_financing + bpp.noncurrent_loans_and_financing)
        net_debt   = gross_debt - bpa.cash_and_cash_equivalents

        total_liabilities = bpp.current_liabilities + bpp.noncurrent_liabilities

        return Indebtedness(
            general_debt              = utils.zero_safe_divide(total_liabilities, bpa.total_assets),
            debt_composition          = utils.zero_safe_divide(bpp.current_liabilities, total_liabilities),
            net_debt_over_net_equity  = utils.zero_safe_divide(net_debt, bpp.net_equity),
            net_debt_over_ebitda      = utils.zero_safe_divide(net_debt, dre.operating_result) if dre.operating_result is not None else None,
            net_debt_over_ebit        = utils.zero_safe_divide(net_debt, dre.operating_profit),
            net_equity_over_assets    = utils.zero_safe_divide(bpp.net_equity, bpa.total_assets),
            cassets_over_cliabilities = utils.zero_safe_divide(bpa.current_assets, bpp.current_liabilities)
        )