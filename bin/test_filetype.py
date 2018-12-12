#!/usr/bin/python
#
#
#
#
# Adriana Toutoudaki (October 2018), contact: adriana.tou@gmail.com

import pandas as pd
import re
import sys
import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Assimilate low res HLA type data.')
parser.add_argument('input', type = argparse.FileType(),  help='input file .xlsx to be analysed')
parser.add_argument('output', help='output file file name to be generated')


#parser.add_argument('f', type=argparse.FileType('r'))
args = parser.parse_args()


input_file = args.input
print (input_file)

output_file = args.output

data = pd.read_excel(args.input, "Main data")


print (data)

