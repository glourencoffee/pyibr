import sys
import zipfile
import icvm
import pprint

def main():
    with zipfile.ZipFile(sys.argv[1]) as file:
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