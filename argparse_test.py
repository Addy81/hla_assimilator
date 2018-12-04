import argparse
import sys
import pandas as pd

'''
parser = argparse.ArgumentParser(description="Find the sum of all the numbers below a certain number.")
parser.add_argument('--below', help='The number to find the sum of numbers below.', type=int, default=1000)

def main():
    args = parser.parse_args()
    s = sum((i for i in range(args.below)))
    print("Sum =", s)
    return 0

if __name__ == "__main__":
    sys.exit(main())





  import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))

'''

parser = argparse.ArgumentParser(description='Assimilate low res HLA type data.')
parser.add_argument('input', help='input file .xlsx to be analysed')
parser.add_argument('output', help='output file file name to be generated')

args = parser.parse_args()

input_file = args.input
output_file = args.output

data = pd.read_excel(input_file, "Main data")

print (data.shape)
print (input_file)