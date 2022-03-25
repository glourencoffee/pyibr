import dataclasses
import collections
import cvm
import typing
import zipfile
from cvm  import csvio, balances, datatypes, exceptions
from icvm import collection

@dataclasses.dataclass(init=True, frozen=True)
class ReaderResult:
    dfpitr: datatypes.DFPITR
    balance_type: datatypes.BalanceType
    indicators: typing.Tuple[collection.IndicatorCollection]

Reader = typing.Generator[ReaderResult, None, None]

def reader(file: zipfile.ZipFile,
           indicator_types: typing.Iterable[collection.IndicatorCollection],
           flag: csvio.BalanceFlag = csvio.BalanceFlag.INDIVIDUAL|csvio.BalanceFlag.CONSOLIDATED
) -> Reader:

    dfpitr_reader   = csvio.dfpitr_reader(file, flag)
    indicator_types = tuple(indicator_types)

    for dfpitr in dfpitr_reader:
        for balance_type in datatypes.BalanceType:
            try:
                statements = dfpitr[balance_type][datatypes.FiscalYearOrder.LAST]
            except KeyError:
                continue

            try:
                industrial = balances.IndustrialCollection.from_statements(statements, balance_type)
            except exceptions.BalanceLayoutError:
                continue

            indicators = []

            for t in indicator_types:
                indicators.append(t.from_industrial(dfpitr, industrial))
            
            yield ReaderResult(dfpitr, balance_type, tuple(indicators))