from b3.net.query import get_detail # FIXME: fix import when b3 library gets published
import dataclasses
import decimal
import typing
import yfinance as yf
from cvm  import balances, datatypes, exceptions
from icvm import collection, utils

@dataclasses.dataclass(init=True, frozen=True)
class Valuation(collection.IndicatorCollection):
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
    def market_data(cls, dfpitr: datatypes.BalanceType) -> typing.Tuple[str, decimal.Decimal, int]:
        raise exceptions.NotImplementedException(cls, 'market_data')

    @classmethod
    def from_industrial(cls, dfpitr: datatypes.BalanceType, industrial: balances.IndustrialCollection):
        bpa = industrial.bpa
        bpp = industrial.bpp
        dre = industrial.dre

        # Market data
        ticker, quote, outstanding_shares = cls.market_data(dfpitr)
        
        # Off-market data
        gross_debt = bpp.current_loans_and_financing + bpp.noncurrent_loans_and_financing
        net_profit = dre.net_profit

        # Indicators
        market_cap = quote * outstanding_shares
        ev         = market_cap + gross_debt - bpa.cash_and_cash_equivalents

        return Valuation(
            ticker                = ticker,
            quote                 = quote,
            outstanding_shares    = outstanding_shares,
            market_capitalization = market_cap,
            enterprise_value      = ev,
            earnings_per_share    = utils.zero_safe_divide(net_profit,     outstanding_shares),
            book_value_per_share  = utils.zero_safe_divide(bpp.net_equity, outstanding_shares),
            ev_ebitda             = utils.none_safe_divide(ev, dre.ebitda),
            ev_ebit               = utils.zero_safe_divide(ev, dre.ebit)
        )

class YfinanceValuation(Valuation):
    @staticmethod
    def market_data_from_ticker(ticker: str, reference_year: int) -> typing.Optional[typing.Tuple[float, int]]:
        start  = f'{reference_year}-12-21'
        end    = f'{reference_year}-12-31'

        quotes = yf.download(ticker, start=start, end=end)

        if quotes.empty:
            return None

        quote  = quotes.iloc[-1]['Close']
        ticker = yf.Ticker(ticker)

        try:
            outstanding_shares = int(ticker.info['sharesOutstanding'])
        except KeyError:
            return None

        return quote, outstanding_shares

    @classmethod
    def market_data(cls, dfpitr: datatypes.BalanceType) -> typing.Tuple[str, decimal.Decimal, int]:
        co = get_detail(dfpitr.cvm_code)

        quote = 0
        outstanding_shares = 0

        for ticker in co.tickers():
            data = YfinanceValuation.market_data_from_ticker(ticker + '.SA', dfpitr.reference_date.year)

            if data is None:
                continue

            # A company may have shares distributed to many instruments, each of which having
            # a different ticker. For example, the Brazilian company ELETROBRAS has 3 tickers
            # on B3: ELET3, ELET5, and ELET6. In order to get the number of outstanding shares
            # of ELETROBRAS, we must sum the outstanding shares in ELE3, ELET5, and ELET6.
            #
            # As for the quote price, each instrument may have a different price, so we choose
            # only the main one, that is, the quote price of `co.trading_code`.

            if ticker == co.trading_code:
                quote = data[0]

            outstanding_shares += data[1]

        return (co.trading_code, decimal.Decimal(quote), outstanding_shares)