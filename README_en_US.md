# About

`ibr` is a Python library that calculates fundamental analysis indicators
of Brazilian companies registered at CVM.

The reason for creating this library is that CVM things must belong to
the [cvm][repo-pycvm] library, whereas fundamental analysis indicators,
insofar they are something greater than CVM, should be separated.

Moreover, valuation indicators depend on market data, which is beyond
CVM's responsibility, since CVM is not a stock exchange.

# Usage

## Financial Indicators

The code below opens a DFP/ITR document and shows financial
indicators of companies in that document:

```py
import ibr

for result in ibr.reader('/path/to/dfp_or_itr.zip', (ibr.Indebtedness, ibr.Profitability, ibr.Efficiency)):
    indebtedness, profitability, efficiency = result.indicators

    print('----------------------------')
    print('Company:', result.dfpitr.company_name)
    
    print('\nIndebtedness:')
    print(indebtedness)
    
    print('\nEfficiency:')
    print(efficiency)
    
    print('\nProfitability:')
    print(profitability)
```

## Valuation Indicators

As for valuation indicators, they need market data. Since market data is
not provided in a DFP/ITR file, because this is beyond CVM's scope, such
data must be obtained from the internet or some other source.

For that, the library `ibr` provides a class `YfinanceValuation`, which
is based on the libraries [b3][repo-pybov] and [yfinance][repo-yfinance]:

```py
import ibr

for result in ibr.reader('/path/to/dfp_or_itr.zip', [ibr.YfinanceValuation]):
    print('------------------')
    print('Company:', result.dfpitr.company_name)
    
    valuations = result.indicators[0]

    for valuation in valuations:
        print('\nValuation:')
        print(valuation)
```

Note that valuation indicators return a list, because it is possible that
a company has more than one security. An example is the company Eletrobrás,
which has three securities on B3: ELET3, ELET5 e ELET6. Since each security
results in different valuation indicators, `valuations` would have 3 objects
for company Eletrobrás.

Another point is that using `YfinanceValuation` is very slow. This is because
the library `yfinance` takes a while to retrieve the shares outstanding of a
company, which is required for calculation.

## Examples

More elaborated examples of usage are in the directory `samples`:

```sh
python -m samples.financial '/path/to/dfp_or_itr.zip'
python -m samples.valuation '/path/to/dfp_or_itr.zip'
```

  [repo-pycvm]: <https://github.com/callmegiorgio/pycvm>
  [repo-pybov]: <https://github.com/callmegiorgio/pybov>
  [repo-yfinance]: <https://pypi.org/project/yfinance/>