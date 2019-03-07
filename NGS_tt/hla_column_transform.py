#!/usr/bin/python3
#
#
#
#
# Adriana Toutoudaki (March 2019), contact: adriana.toutoudaki@addenbrookes.nhs.uk

import pandas as pd
import re
import argparse
import os
from termcolor import colored



parser = argparse.ArgumentParser (description = 'Transform tranfer tab into a table.')
parser.add_argument('input',help = 'file to be transformed')
args = parser.parse_args()
input_file = args.input

dir_path = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.basename(input_file).replace(".xlsx", "_to_test.xlsx")

data = pd.read_excel(input_file, "Transfer")

rn = data.shape[0]

patients = []
types = []

for r in range(rn):
    if data.loc[r,'Name'] not in patients:
        patients.append(data.loc[r,'Name'])
    if data.loc[r,'Component'] not in types:
        types.append(data.loc[r,'Component'])
    else:
        pass

patient_types = {}
for patient in patients:
    type_list = []
    for r in range(rn):
    #for tp in types:
        if data.loc[r,'Name'] == patient:
            hla_type = data.loc[r,'Result']
            type_list.append(hla_type)
    
        patient_types[patient] = type_list

#for key in patient_types.keys():
#    print (len(patient_types[key]))

df = pd.DataFrame.from_dict(patient_types,orient='index',columns=['Recip_First_A_Split','Recip_Second_A_Split','Recip_First_B_Split','Recip_Second_B_Split','Recip_First_C_Split','Recip_Second_C_Split','DPA1','DPA2' ,'DPB1','DPB2', 'DQA1','DQA2', 'Recip_First_DQ_Split','Recip_Second_DQ_Split','Recip_First_DR_Split','Recip_Second_DR_Split','DRB345-1','DRP345-2'])


def add_letter(gene):

    first_col = 'Recip_First_' + gene + '_Split'
    second_col = 'Recip_Second_' + gene + '_Split'
    #index1 = df.columns.get_loc(first_col)
    #index2 = df.columns.get_loc(second_col)

    patterns = [first_col,second_col]

    for row in range(df.shape[0]):
        for pattern in patterns:
            
            col_index = df.columns.get_loc(pattern)
            
            for column in df.columns:
                if re.match(pattern,column):
                    cell = df.iloc[row][column]
                    cell = str(cell).strip()
                    if gene == 'C':
                        cell = gene + 'w' + cell
                        df.iat[row,col_index] = cell
                    else:
                        cell = gene + cell
                        df.iat[row,col_index] = cell
            
genes = ['A','B','C','DQ','DR']

for gene in genes:
    add_letter(gene)

writer = pd.ExcelWriter(output_file, engine = 'xlsxwriter')
df.to_excel(writer, sheet_name = 'Test Set')

writer.save()


print(colored('SUCCESS!', 'green'))