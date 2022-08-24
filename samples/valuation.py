"""Valuation Sample.

Usage:
  indicators <dfpitr>
  indicators --help

Options:
  --help  Show this screen.
"""

import cvm
import docopt
import icvm
import pandas as pd
import sys
import zipfile

def main():
    args = docopt.docopt(__doc__)

    filepath = args['<dfpitr>']

    with zipfile.ZipFile(filepath) as file:
        reader = icvm.reader(file, [icvm.YfinanceValuation], flag=cvm.csvio.BalanceFlag.CONSOLIDATED)

        for res in reader:
            for valuation in res.indicators:
                print('------------------')
                print('Company:', res.dfpitr.company_name)
                
                print('\nValuation:')
                print(pd.DataFrame([valuation]).transpose()[0].to_string())

    return 0

if __name__ == '__main__':
    sys.exit(main())