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
parser.add_argument('input', default=sys.stdin, help='input file .xlsx to be analysed')
parser.add_argument('output', help='output file file name to be generated')


#parser.add_argument('f', type=argparse.FileType('r'))
args = parser.parse_args()

input_file =args.input
#print (input_file)

output_file = args.output

data = pd.read_excel(input_file, "Main data")

rules_file = './HLA_rules.xlsx'


#data = pd.read_excel(data_file, "Main data")
#rules = pd.read_excel(rules_file)

# print (data)
# make rules lists
#A_LR = (rules.loc[:20,'HLA-A']).tolist()
#A_HR = (rules.loc[:20,'Assimilation']).tolist()


# fill_split function iterates through the columns containing the HLA data and fills the split column
# with the equivalent broad if empty

def fill_split(patient):
    gene_list= ["A","B","C","DR","DP","DQ"]
    for gene in gene_list:
        for column in data.columns:
            first_split = patient + '_First_' + gene + '_Split'
            first_broad = patient + '_First_' + gene + '_Broad'
            second_split = patient + '_Second_' + gene + '_Split'
            second_broad = patient + '_Second_' + gene + '_Broad'

            #Match column names above to select the correct one to populate

            x = re.match(first_split, column)
            y = re.match(second_split, column)

            if x:
                data[first_split] = data[first_split].fillna(data[first_broad])
            elif y:
                data[second_split] = data[second_split].fillna(data[second_broad])


# Run function for Recipient and Donor data
fill_split('Recip')
fill_split('Donor')


# hard-coded list of rules. This can be parsed to the script instead if preferred.

# A_LR = rules.loc[:20,'A_LR'].tolist()
# A_HR = rules.loc[:20,'A_HR'].tolist()
A_LR = ['A1', 'A2', 'A3', 'A11', 'A23', 'A24', 'A25', 'A26', 'A29', 'A30', 'A31', 'A32', 'A33', 'A34', 'A36', 'A43', 'A66', 'A68', 'A69', 'A74', 'A80']
A_HR = ['A*01:01', 'A*02:01', 'A*03:01', 'A*11:01', 'A*23:01', 'A*24:02', 'A*25:01', 'A*26:01', 'A*29:02', 'A*30:01', 'A*31:01', 'A*32:01', 'A*33:01', 'A*34:01', 'A*36:01', 'A*43:01', 'A*66:01', 'A*68:01', 'A*69:01', 'A*74:01', 'A*80:01']

# B_LR = rules.loc[:45,'B_LR'].tolist()
# B_HR = rules.loc[:45,'B_HR'].tolist()
B_LR = ['B7', 'B8', 'B13', 'B64', 'B65', 'B62', 'B75', 'B72', 'B71', 'B76', 'B77', 'B63', 'B18', 'B27', 'B35', 'B37', 'B38', 'B39', 'B60', 'B61', 'B40', 'B41', 'B42', 'B44', 'B45', 'B46', 'B47', 'B48', 'B49', 'B50', 'B51', 'B52', 'B53', 'B54', 'B55', 'B56', 'B57', 'B58', 'B59', 'B67', 'B73', 'B78', 'B81', 'B82']
B_HR = ['B*07:02', 'B*08:01', 'B*13:01', 'B*14:01', 'B*14:02', 'B*15:01', 'B*15:02', 'B*15:03', 'B*15:10', 'B*15:12', 'B*15:13', 'B*15:16', 'B*18:01', 'B*27:05', 'B*35:01', 'B*37:01', 'B*38:01', 'B*39:01', 'B*40:01', 'B*40:02', 'B*40:05', 'B*41:01', 'B*42:01', 'B*44:02', 'B*45:01', 'B*46:01', 'B*47:01', 'B*48:01', 'B*49:01', 'B*50:01', 'B*51:01', 'B*52:01', 'B*53:01', 'B*54:01', 'B*55:01', 'B*56:01', 'B*57:01', 'B*58:01', 'B*59:01', 'B*67:01', 'B*73:01', 'B*78:01', 'B*81:01', 'B*82:01']

# C_LR = rules.loc[:17,'C_LR'].tolist()
# C_HR = rules.loc[:17,'C_HR'].tolist()

# C rules- simple. The Cw/B pairings need to be added.
C_LR = ["Cw1","Cw2","Cw4","Cw9","Cw5","Cw6","Cw12","Cw14","Cw15","Cw17","Cw18",]
C_HR = ["C*01:02","C*02:02","C*04:01","C*03:03","C*05:01","C*06:02","C*12:03","C*14:02","C*15:02","C*17:01","C*18:01",]


# replace

# Copy split column and rename it to with an HR_ prefix
for column in data.columns:
    column_check = re.search('_Split', column)
    col_index = data.columns.get_loc(column)
    new_column_name = "HR_" + column
    if column_check:
        data.insert((col_index + 1), new_column_name, data[column])

# when there's the first Cw present - assume homozygous so fill the Second Split column


def fill_hom(patient, gene):
    first = 'HR_' + patient + '_First_'+ gene + '_Split'
    second =  'HR_' + patient + '_Second_'+ gene + '_Split'

    for column in data.columns:
        f = re.match(second, column)
        if f:
            data[second] = data[second].fillna(data[first])
        else:
            pass


fill_hom('Recip', 'C')
fill_hom('Donor', 'C')

fill_hom('Recip', 'DQ')
fill_hom('Donor', 'DQ')

# Replace low-res alleles in the HR_ columns using the rule lists above

for column in data.columns:
    column_check = re.match('HR_', column)
    if column_check:
        data[column].replace(to_replace = A_LR, value = A_HR, inplace = True)
        data[column].replace(to_replace = B_LR, value = B_HR, inplace = True)
        data[column].replace(to_replace = C_LR, value = C_HR, inplace = True)
    else:
        pass


# special Cw/B pairing replacement
# Function that replaces Cw alleles based on the B allele correlation


rows = data.shape[0]

def c_assimilation(to_replace, general_rule, exc1, exc2=(None, None),exc3=(None, None)):
    for patient in ['Recip', 'Donor']:
        for variable in ['First', 'Second']:
            #rows = data.shape[0]
            for row in range(rows):
                c_col = "HR_" + patient + '_' + variable + '_C_Split'
                b1_col = "HR_" + patient + '_First_B_Split'
                b2_col = "HR_" + patient + '_Second_B_Split'

                c = data.loc[row, c_col]
                b1 = data.iloc[row][b1_col]
                b2 = data.iloc[row][b2_col]

                if pd.isnull(data.loc[row, c_col]):
                    pass
                elif c == to_replace and ((b1 == exc1[0]) or (b2 == exc1[0])):
                    data.loc[row, c_col] = re.sub(to_replace, exc1[1], c)
                elif c == to_replace and ((b1 == exc2[0]) or (b2 == exc2[0])):
                    data.loc[row, c_col] = re.sub(to_replace, exc2[1], c)
                elif c == to_replace and ((b1 == exc3[0]) or (b2 == exc3[0])):
                    data.loc[row, c_col] = re.sub(to_replace, exc2[1], c)
                else:
                    data.loc[row, c_col] = re.sub(to_replace, general_rule, c)


# Function that replaces Cw alleles based on the B allele correlation
# format of function is
# to_replace - CwX : the low res allele to be substituted
# general_rule : C*xx:xx :the most common high-res allele
# exc1,exc2,exc3: tuple that contains the associated B allele with the special C to replace. (B*xx:xx,C*xx:xx)


c_assimilation(to_replace='Cw10', general_rule='C*03:02', exc1=('B*40:01', 'C*03:04'), exc2=('B*15:01', 'C*03:04'))
c_assimilation(to_replace='Cw8', general_rule='C*08:01', exc1=('B*14:01', 'C*08:02'), exc2=('B*14:02', 'C*08:02'))
c_assimilation(to_replace='Cw16', general_rule='C*16:01', exc1=('B*44:03', 'C*16:02'), exc2=('B*55:01', 'C*16:02'))
c_assimilation(to_replace='Cw7', general_rule='C*07:01', exc1=('B*07:02', 'C*07:02'))


#add a DR51/52/53 column

column_patterns = ['Recip_First', 'Recip_Second', 'Donor_First', 'Donor_Second']

for c_pat in column_patterns:
    for column in data.columns:
        dr_pattern = 'HR_' + c_pat + '_DR_Split'
        column_match = re.match(dr_pattern, column)
        col_index = data.columns.get_loc(dr_pattern)
        if column_match:
            new_dr_column = 'HR_' + c_pat + '_DRB3/4/5'
            data.insert((col_index+1),new_dr_column,np.nan)

for c_pat in column_patterns:
    for column in data.columns:
        dqa_pattern = 'HR_' + c_pat + '_DQ_Split'
        column_match = re.match(dqa_pattern, column)
        col_index = data.columns.get_loc(dqa_pattern)
        if column_match:
            new_dq_column = 'HR_' + c_pat + '_DQA'
            data.insert((col_index + 1), new_dq_column, np.nan)

rules = pd.read_excel('classII_rules.xlsx')

# create a list containing all class II rules


classII = []
rule_rows = rules.shape[0]
for row in range(rule_rows):
    row_sublist = []
    for column in rules.columns:
        row_sublist.append(rules.loc[row][column])
    classII.append(row_sublist)


''''
for c_pat in column_patterns:
    dr_col = 'HR_' + c_pat + '_DR_Split'
    dq_col = 'HR_' + c_pat + '_DQ_Split'
    drb_col = 'HR_' + c_pat + '_DRB3/4/5'
    dqa_col = 'HR_' + c_pat + '_DQA'

    for row in range(rows):
        dr = data.loc[row, dr_col]
        dq = data.loc[row, dq_col]

        for rule in classII:
            if pd.isnull(data.loc[row, dr_col]):
                pass
            elif dr == rule[0] and dq == rule[4]:

'''

# save file into a different excel file
writer = pd.ExcelWriter(output_file, engine = 'xlsxwriter')

data.to_excel(writer,sheet_name='Main data')
writer.save()