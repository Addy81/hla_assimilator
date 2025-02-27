# !/usr/bin/python
#
#
#
#
# Adriana Toutoudaki (December 2018), contact: adriana.tou@gmail.com

import pandas as pd
import re
import sys
import numpy as np

data = pd.read_excel('../data/classII_only.xlsx')
rows = data.shape[0]


options = {
    "DR1": ["DQ5"],
    "DR103": ["DQ5", "DQ7"],
    "DR4": ["DQ7", "DQ8", "DQ4"],
    "DR7": ["DQ2", "DQ9"],
    "DR8": ["DQ4", "DQ7", "DQ6"],
    "DR9": ["DQ2", "DQ9"],
    "DR10": ["DQ5"],
    "DR11": ["DQ6", "DQ7"],
    "DR12": ["DQ5", "DQ7"],
    "DR13": ["DQ2", "DQ6", "DQ7"],
    "DR14": ["DQ5", "DQ7"],
    "DR15": ["DQ6", "DQ5"],
    "DR16": ["DQ5"],
    "DR17": ["DQ2"],
    "DR18": ["DQ4"]
}


rules = pd.read_excel('../data/classII_rules.xlsx')

classII = []
rule_rows = rules.shape[0]
count = 1
for row in range(rule_rows):
    row_sublist = [count]
    count += 1
    for column in rules.columns:
        row_sublist.append(rules.loc[row][column])
    classII.append(row_sublist)

classIIb = classII.copy()

for x in classII:
    print(x)

def fill_hom(patient, gene):
    """Assuming when only one allele present it is homozygous
    so this function fills in the equivalent homozygous allele"""

    first = 'HR_' + patient + '_First_' + gene + '_Split'
    second = 'HR_' + patient + '_Second_' + gene + '_Split'

    for column in data.columns:
        f = re.match(second, column)
        if f:
            data[second] = data[second].fillna(data[first])
        else:
            pass


fill_hom('Recip', 'DQ')
fill_hom('Donor', 'DQ')

for key in options.keys():
    print(key, '-->', options[key])

DR_columns = ["HR_Recip_First_DR_Split", "HR_Recip_Second_DR_Split"]

print(rows)
print("---------------------------------------------------------------------------")

# Swap columns around to allow for the one with only one option to be first

for row in range(rows):
    count1 = 0
    count2 = 0
    DR1 = data.loc[row, "HR_Recip_First_DR_Split"]
    DR2 = data.loc[row, "HR_Recip_Second_DR_Split"]
    DQ1 = data.loc[row, "HR_Recip_First_DQ_Split"]
    DQ2 = data.loc[row, "HR_Recip_Second_DQ_Split"]

    if DR1 in options.keys() and DR2 in options.keys():
        if DQ1 in options.get(DR1):
            count1 = count1 + 1
        if DQ2 in options.get(DR1):
            count1 = count1 + 1
        if DQ1 in options.get(DR2):
            count2 = count2 + 1
        if DQ2 in options.get(DR2):
            count2 = count2 + 1
    # elif type(DQ1) == float or type(DQ2) == float:
    # pass
    if count1 > 1 and count2 < 2:
        data.loc[row, "HR_Recip_First_DR_Split"] = DR2
        data.loc[row, "HR_Recip_Second_DR_Split"] = DR1

# USe it when we are back in normal dataset
def add_sub_column(patient):
    """Adds column to store substitution codes"""

    pattern = patient + "_First_DR_Broad"
    for column in data.columns:
        column_match = re.match(pattern,column)
        col_index = data.columns.get_loc(pattern)
        if column_match:
            new_column = patient + "_First_Sub"
            new_column2 = patient + "_Second_Sub"
            data.insert(col_index, new_column,np.nan)
            data.insert(col_index+6, new_column2, np.nan)

add_sub_column("Recip")

#print (data.columns)

for row in range(rows):
    DR1 = data.loc[row, "HR_Recip_First_DR_Split"]
    DR2 = data.loc[row, "HR_Recip_Second_DR_Split"]
    DQ1 = data.loc[row, "HR_Recip_First_DQ_Split"]
    DQ2 = data.loc[row, "HR_Recip_Second_DQ_Split"]
    first_sub = "Recip_First_Sub"
    second_sub = "Recip_Second_Sub"

    dq_options = [DQ1,DQ2]

    while len(dq_options) > 0:
        if dq_options[0] in options.get(DR1):
            # print (dq_options[0], "-->", DR1)
            for rule in classII:
                if rule[1] == DR1 and rule[5] == DQ1:
                    # print (rule[1],rule[5])
                    data.loc[row, first_sub] = "a" + str(rule[0])
                    del dq_options[0]
                    break
            if dq_options[0] in options.get(DR2):
                for rule in classII:
                    if rule[1] == DR2 and rule[5] == DQ2:
                        data.loc[row,second_sub] = "a" + str(rule[0])
                        del dq_options[0]
        elif dq_options[1] in options.get(DR1):
            for rule in classII:
                if rule[1] == DR1 and rule[5] == DQ2:
                    data.loc[row, first_sub] = "b" + str(rule[0])
                    del dq_options[1]
                    break
            if dq_options[0] in options.get(DR2):
                for rule in classII:
                    if rule[1] == DR2 and rule[5] == DQ1:
                        data.loc[row, second_sub] = "b" + str(rule[0])
                        del dq_options[0]


print (data["Recip_First_Sub"])


