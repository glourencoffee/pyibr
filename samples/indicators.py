"""Indicators Sample

Usage:
  indicators <dfpitr>
  indicators --help

Options:
  --help  Show this screen.
"""

import docopt
import icvm
import pprint
import sys
import time
import zipfile

def main():
    args = docopt.docopt(__doc__)

    filepath = args['<dfpitr>']

    with zipfile.ZipFile(filepath) as file:
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

            time.sleep(2)

    return 0

if __name__ == '__main__':
    sys.exit(main())