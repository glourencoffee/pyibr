# About

`icvm` is a Python library that calculates fundamental analysis indicators from companies registered at CVM.

The purpose for creating this library is that CVM stuff must pertain to the `cvm` library, whereas fundamental
analysis indicators, insofar they are something greater than CVM itself, should be separate. Moreover, valuation
indicators rely on market data, which lies beyond CVM's responsibility, since CVM is not an exchange.

# Usage

```py
import icvm
import zipfile

with zipfile.ZipFile('/path/to/dfp_or_itr.zip') as file:
    reader = icvm.reader(file, (icvm.Indebtedness, icvm.Profitability, icvm.Efficiency))

    for res in reader:
        indebtedness, profitability, efficiency = res.indicators

        print('----------------------------')
        print('Company:', res.dfpitr.company_name)
        
        print('\nIndebtedness:')
        print(indebtedness.series())
        
        print('\nEfficiency:')
        print(efficiency.series())
        
        print('\nProfitability:')
        print(profitability.series())
```

As for valuation indicators, they need market data, which are beyond the scope of CVM.
As such, market data must be retrieved from the internet or some other source.

`icvm` provides a class `YfinanceValuation`, which is based on the libraries `yfinance` and `b3`:

```py
import icvm
import zipfile

with zipfile.ZipFile('/path/to/dfp_or_itr.zip') as file:
    reader = icvm.reader(file, [icvm.YfinanceValuation])

    for res in reader:
        valuation = res.indicators[0]

        print('------------------')
        print('Company:', res.dfpitr.company_name)
        
        print('\nValuation:')
        print(valuation.series())
```

Note that using `YfinanceValuation` is slow as fuck. This is because `yfinance` takes a while to
retrieve the number of outstanding shares of a company, which is required to calculate valuation indicators.