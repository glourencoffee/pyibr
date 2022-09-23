import ibr
import pandas as pd
import sys

def main():
    if len(sys.argv) < 2:
        print('usage: indicators.py <dfpitr>')
        return 1
    
    filepath = sys.argv[1]

    try:
        for result in ibr.reader(filepath, [ibr.YfinanceValuation]):
            for valuation in result.indicators[0]:
                print('------------------')
                print('Company:', result.dfpitr.company_name)

                print('\nValuation:')
                print(pd.DataFrame([valuation]).transpose()[0].to_string())
    except KeyboardInterrupt:
        pass

    return 0

if __name__ == '__main__':
    sys.exit(main())