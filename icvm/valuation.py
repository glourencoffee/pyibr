from __future__ import annotations
import b3
import cvm
import dataclasses
import datetime
import decimal
import typing
import yfinance as yf
from icvm import utils

@dataclasses.dataclass(init=True)
class Valuation:
    ticker: str
    """'Código de negociação'"""

    quote: decimal.Decimal
    """'Cotação'"""

    outstanding_shares: int
    """'Ações em circulação'"""

    market_capitalization: decimal.Decimal
    """'Valor de Mercado'"""

    enterprise_value: decimal.Decimal
    """'Valor da Firma'"""

    earnings_per_share: decimal.Decimal
    """'Lucro por Ação' (LPA)"""

    book_value_per_share: decimal.Decimal
    """'Valor Patrimonial da Ação' (VPA)"""

    ev_ebitda: typing.Optional[decimal.Decimal]
    """EV/EBITDA"""

    ev_ebit: decimal.Decimal
    """EV/EBIT"""

    @property
    def market_cap(self) -> decimal.Decimal:
        """Same as `market_capitalization`."""

        return self.market_capitalization

    @property
    def ev(self) -> decimal.Decimal:
        """Same as `enterprise_value`."""

        return self.enterprise_value

    @property
    def eps(self) -> decimal.Decimal:
        """Same as `earnings_per_share`."""

        return self.earnings_per_share

    @property
    def bvps(self) -> decimal.Decimal:
        """Same as `book_value_per_share`."""

        return self.book_value_per_share

    @classmethod
    def market_data(cls, cvm_code: int, reference_date: datetime.date) -> typing.Iterable[typing.Tuple[str, decimal.Decimal, int]]:
        raise NotImplementedError(f"method 'market_data' of {cls}")

    @classmethod
    def from_statement(cls,
                       cvm_code: int,
                       reference_date: datetime.date,
                       balance_sheet: cvm.balances.BalanceSheet,
                       income_statement: cvm.balances.IncomeStatement
    ) -> typing.List[Valuation]:
        b = balance_sheet
        i = income_statement

        # Off-market data
        net_debt = b.net_debt or 0
        valuations = []

        # Market data
        for ticker, quote, outstanding_shares in cls.market_data(cvm_code, reference_date):
            market_cap = quote * outstanding_shares
            ev         = market_cap + net_debt

            valuations.append(
                Valuation(
                    ticker                = ticker,
                    quote                 = quote,
                    outstanding_shares    = outstanding_shares,
                    market_capitalization = market_cap,
                    enterprise_value      = ev,
                    earnings_per_share    = utils.zero_safe_divide(i.net_income, outstanding_shares),
                    book_value_per_share  = utils.zero_safe_divide(b.equity,     outstanding_shares),
                    ev_ebitda             = utils.none_safe_divide(ev,           i.ebitda),
                    ev_ebit               = utils.zero_safe_divide(ev,           i.ebit)
                ))

        return valuations

class YfinanceValuation(Valuation):
    @staticmethod
    def market_data_from_ticker(ticker: str, reference_year: int) -> typing.Optional[typing.Tuple[float, int]]:
        start  = f'{reference_year}-01-01'
        end    = f'{reference_year}-12-31'

        quotes = yf.download(ticker, start=start, end=end)

        if quotes.empty:
            return None

        quote  = quotes.iloc[-1]['Close']
        ticker = yf.Ticker(ticker)

        try:
            # Yahoo Finance only stores `sharesOutstanding` for the last
            # quarterly statement provided by the company, so `reference_year`
            # will be ignored...
            outstanding_shares = int(ticker.info['sharesOutstanding'])
        except KeyError:
            return None

        return quote, outstanding_shares

    @classmethod
    def market_data(cls, cvm_code: int, reference_date: datetime.date) -> typing.Iterable[typing.Tuple[str, decimal.Decimal, int]]:
        co = b3.net.query_company(cvm_code)

        for codes in co.security_codes:
            data = YfinanceValuation.market_data_from_ticker(codes.ticker + '.SA', reference_date.year)

            if data is None:
                continue

            quote, outstanding_shares = data

            yield (codes.ticker, decimal.Decimal(quote), outstanding_shares)