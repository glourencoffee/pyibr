"""Valuation Sample.

Usage:
  indicators <dfpitr>
  indicators --help

Options:
  --help  Show this screen.
"""

import docopt
import icvm
import sys
import zipfile

def main():
    args = docopt.docopt(__doc__)

    filepath = args['<dfpitr>']

    with zipfile.ZipFile(filepath) as file:
        reader = icvm.reader(file, [icvm.YfinanceValuation])

        for res in reader:
            valuation = res.indicators[0]

            print('------------------')
            print('Company:', res.dfpitr.company_name)
            
            print('\nValuation:')
            print(valuation.series())

    return 0

if __name__ == '__main__':
    sys.exit(main())