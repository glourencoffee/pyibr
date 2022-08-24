"""Indicators Sample.

Usage:
  indicators <dfpitr>
  indicators --help

Options:
  --help  Show this screen.
"""

import docopt
import icvm
import pandas as pd
import time
import sys
import zipfile

def print_indicator(i):
    print(f'\n{i.__class__.__name__}:')
    print(pd.DataFrame([i]).transpose()[0].to_string())

def main():
    args = docopt.docopt(__doc__)

    filepath = args['<dfpitr>']

    with zipfile.ZipFile(filepath) as file:
        reader = icvm.reader(file, (icvm.Indebtedness, icvm.Profitability, icvm.Efficiency))

        for res in reader:
            indebtedness, profitability, efficiency = res.indicators

            print('----------------------------')
            print(f'Company: {res.dfpitr.company_name} ({res.balance_type})')
            
            print_indicator(indebtedness)
            print_indicator(efficiency)
            print_indicator(profitability)

            time.sleep(2)

    return 0

if __name__ == '__main__':
    sys.exit(main())