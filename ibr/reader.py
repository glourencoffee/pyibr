import cvm
import dataclasses
import datetime
import ibr
import os
import typing
import zipfile

Indicator = typing.Union[ibr.Indebtedness, ibr.Efficiency, ibr.Profitability, ibr.Valuation]

@dataclasses.dataclass(init=True)
class ReaderResult:
    dfpitr: cvm.DFPITR
    balance_type: cvm.BalanceType
    indicators: typing.List[Indicator]

Reader = typing.Generator[ReaderResult, None, None]

def from_statement(cvm_code: int,
                   reference_date: datetime.date,
                   balance_sheet: cvm.BalanceSheet,
                   income_statement: cvm.IncomeStatement,
                   indicator_types: typing.Iterable[typing.Type[Indicator]]
) -> typing.List[Indicator]:
    indicators = []

    for cls in indicator_types:
        if issubclass(cls, (ibr.Indebtedness, ibr.Profitability)):
            indicators.append(cls.from_statement(balance_sheet, income_statement))
        elif issubclass(cls, ibr.Efficiency):
            indicators.append(cls.from_statement(income_statement))
        elif issubclass(cls, ibr.Valuation):
            indicators.append(cls.from_statement(cvm_code, reference_date, balance_sheet, income_statement))
        else:
            raise TypeError(f'{cls} is not an indicator class')

    return indicators

def reader(file: typing.Union[zipfile.ZipFile, typing.IO, os.PathLike, str],
           indicator_types: typing.Iterable[typing.Type[Indicator]]
) -> Reader:

    dfpitr_reader   = cvm.dfpitr_reader(file, cvm.BalanceFlag.CONSOLIDATED)
    indicator_types = tuple(indicator_types)

    for dfpitr in dfpitr_reader:
        try:
            balance_sheet    = cvm.BalanceSheet.from_dfpitr(dfpitr)
            income_statement = cvm.IncomeStatement.from_dfpitr(dfpitr)
        except ValueError:
            continue
        else:
            indicators = from_statement(
                dfpitr.cvm_code,
                dfpitr.reference_date,
                balance_sheet,
                income_statement,
                indicator_types
            )

            yield ReaderResult(dfpitr, cvm.BalanceType.CONSOLIDATED, indicators)