import cvm
import dataclasses
import datetime
import icvm
import os
import typing
import zipfile

Indicator = typing.Union[icvm.Indebtedness, icvm.Efficiency, icvm.Profitability, icvm.Valuation]

@dataclasses.dataclass(init=True)
class ReaderResult:
    dfpitr: cvm.datatypes.DFPITR
    balance_type: cvm.datatypes.BalanceType
    indicators: typing.List[Indicator]

Reader = typing.Generator[ReaderResult, None, None]

def from_statement(cvm_code: int,
                   reference_date: datetime.date,
                   balance_sheet: cvm.balances.BalanceSheet,
                   income_statement: cvm.balances.IncomeStatement,
                   indicator_types: typing.Iterable[typing.Type[Indicator]]
) -> typing.List[Indicator]:
    indicators = []

    for cls in indicator_types:
        if issubclass(cls, (icvm.Indebtedness, icvm.Profitability)):
            indicators.append(cls.from_statement(balance_sheet, income_statement))
        elif issubclass(cls, icvm.Efficiency):
            indicators.append(cls.from_statement(income_statement))
        elif issubclass(cls, icvm.Valuation):
            indicators.append(cls.from_statement(cvm_code, reference_date, balance_sheet, income_statement))
        else:
            raise TypeError(f'{cls} is not an indicator class')

    return indicators

def reader(file: typing.Union[zipfile.ZipFile, typing.IO, os.PathLike, str],
           indicator_types: typing.Iterable[typing.Type[Indicator]],
           flag: cvm.csvio.BalanceFlag = cvm.csvio.BalanceFlag.INDIVIDUAL|cvm.csvio.BalanceFlag.CONSOLIDATED
) -> Reader:

    dfpitr_reader   = cvm.csvio.dfpitr_reader(file, flag)
    indicator_types = tuple(indicator_types)

    for dfpitr in dfpitr_reader:
        for balance_type in cvm.datatypes.BalanceType:

            try:
                balance_sheet    = cvm.balances.BalanceSheet.from_document(dfpitr, balance_type)
                income_statement = cvm.balances.IncomeStatement.from_document(dfpitr, balance_type)
            except KeyError:
                continue
            else:
                indicators = from_statement(
                    dfpitr.cvm_code,
                    dfpitr.reference_date,
                    balance_sheet,
                    income_statement,
                    indicator_types
                )

                yield ReaderResult(dfpitr, balance_type, indicators)