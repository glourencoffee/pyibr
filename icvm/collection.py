from __future__ import annotations
import decimal
import pandas as pd
import typing
from cvm import balances, datatypes, exceptions

class IndicatorCollection:
    @classmethod
    def from_industrial(cls, dfpitr: datatypes.BalanceType, industrial: balances.IndustrialCollection) -> IndicatorCollection:
        """Creates an indicator collection from an industrial balance."""

        raise exceptions.NotImplementedException(cls, 'from_industrial')

    def series(self, decimals: int = 2) -> pd.Series:
        return pd.Series(self.dump(decimals))

    def dump(self, decimals: int = 2) -> typing.Dict[str, typing.Any]:
        """Returns a dict of the values stored by this indicator collection
        rounded to `decimals` decimal places, mapped to its attribute names."""

        obj = {}

        for k, v in vars(self).items():
            if isinstance(v, (float, decimal.Decimal)):
                v = round(v, decimals)
            
            obj[k] = v

        return obj