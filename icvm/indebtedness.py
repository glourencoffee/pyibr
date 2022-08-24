from __future__ import annotations
import dataclasses
import decimal
import typing
import cvm
from icvm import utils

@dataclasses.dataclass(init=True)
class Indebtedness:
    general_debt: decimal.Decimal
    """'Dívida Geral'"""

    debt_composition: decimal.Decimal
    """'Composição da Dívida' (CD)"""

    net_debt_to_equity: decimal.Decimal
    """'Dívida Líquida/Patrimônio Líquido'"""
    
    net_debt_to_ebitda: typing.Optional[decimal.Decimal]
    """'Dívida Líquida/EBITDA'"""
    
    net_debt_to_ebit: decimal.Decimal
    """'Dívida Líquida/EBIT'"""

    net_equity_to_assets: decimal.Decimal
    """'Dívida Líquida/Ativo'"""
    
    current_ratio: decimal.Decimal
    """'Ativo/Passivo'"""

    @staticmethod
    def from_statement(balance_sheet: cvm.balances.BalanceSheet,
                       income_statement: cvm.balances.IncomeStatement
    ) -> Indebtedness:
        b = balance_sheet
        i = income_statement

        return Indebtedness(
            general_debt         = utils.zero_safe_divide(b.total_liabilities,   b.total_assets),
            debt_composition     = utils.none_safe_divide(b.current_liabilities, b.total_liabilities),
            net_debt_to_equity   = utils.none_safe_divide(b.net_debt,            b.equity),
            net_debt_to_ebitda   = utils.none_safe_divide(b.net_debt,            i.ebitda),
            net_debt_to_ebit     = utils.none_safe_divide(b.net_debt,            i.ebit),
            net_equity_to_assets = utils.zero_safe_divide(b.equity,              b.total_assets),
            current_ratio        = utils.none_safe_divide(b.current_assets,      b.current_liabilities)
        )