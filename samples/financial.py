import icvm
import pandas as pd
import time
import sys

def print_indicator(i):
    print(f'\n{i.__class__.__name__}:')
    print(pd.DataFrame([i]).transpose()[0].to_string())

def main():
    if len(sys.argv) < 2:
        print('usage: financial.py <dfpitr>')
        return 1
    
    filepath = sys.argv[1]

    try:
        for result in icvm.reader(filepath, (icvm.Indebtedness, icvm.Profitability, icvm.Efficiency)):
            indebtedness, profitability, efficiency = result.indicators

            print('----------------------------')
            print(f'Company: {result.dfpitr.company_name} ({result.balance_type})')
            
            print_indicator(indebtedness)
            print_indicator(efficiency)
            print_indicator(profitability)

            time.sleep(2)
    except KeyboardInterrupt:
        pass

    return 0

if __name__ == '__main__':
    sys.exit(main())