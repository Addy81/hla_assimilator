# !/usr/bin/python
#
#
#
#
# Adriana Toutoudaki (October 2018), contact: adriana.tou@gmail.com


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

# create a list containing all class II rules


classII = []
rule_rows = rules.shape[0]
for row in range(rule_rows):
    row_sublist = []
    for column in rules.columns:
        row_sublist.append(rules.loc[row][column])
    classII.append(row_sublist)

classIIb = classII.copy()
for x in classII:
    print(x)

def fill_hom(patient, gene):
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

    # print(DR1,'matched', count1, 'time(s)',  DR2,'matched', count2, 'time(s)', '-------', DQ1,DQ2)

# print (data["HR_Recip_First_DR_Split"],data["HR_Recip_Second_DR_Split"])

'''
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

    # print(DR1,'matched', count1, 'time(s)',  DR2,'matched', count2, 'time(s)', '-------', DQ1,DQ2)
'''
print(type(classII))
for row in range(rows):
    DR1 = data.loc[row, "HR_Recip_First_DR_Split"]
    DR2 = data.loc[row, "HR_Recip_Second_DR_Split"]
    DQ1 = data.loc[row, "HR_Recip_First_DQ_Split"]
    DQ2 = data.loc[row, "HR_Recip_Second_DQ_Split"]

    #dq_options = [data.loc[row, "HR_Recip_First_DQ_Split"], data.loc[row, "HR_Recip_Second_DQ_Split"]]
    dq_options = [DQ1,DQ2]
    print(DR1, DR2)
    print(dq_options)

    while len(dq_options) > 0:
        if dq_options[0] in options.get(DR1):
            for rule in classII:
                if rule[0] == DR1 and rule[4] == DQ1:
                    data.loc[row, "HR_Recip_First_DR_Split"] = rule[1]
                    data.loc[row, "HR_Recip_First_DRB3/4/5"] = rule[3]
                    data.loc[row, "HR_Recip_First_DQ_Split"] = rule[5]
                    data.loc[row, "HR_Recip_First_DQA"] = rule[6]
                    print('Option 1',DR1,
                          data.loc[row, "HR_Recip_First_DR_Split"],
                          data.loc[row, "HR_Recip_First_DRB3/4/5"],
                          data.loc[row, "HR_Recip_First_DQ_Split"], DQ1,
                          data.loc[row, "HR_Recip_First_DQA"])
                    del dq_options[0]
                    print("Test1",dq_options)
                    break
            if dq_options[0] in options.get(DR2):
                for rule in classII:
                    if rule[0] == DR2 and rule[4] == DQ2:
                        data.loc[row, "HR_Recip_Second_DR_Split"] = rule[1]
                        data.loc[row, "HR_Recip_Second_DRB3/4/5"] = rule[3]
                        data.loc[row, "HR_Recip_Second_DQ_Split"] = rule[5]
                        data.loc[row, "HR_Recip_Second_DQA"] = rule[6]
                        print('Option 2',DR2,
                              data.loc[row, "HR_Recip_Second_DR_Split"],
                              data.loc[row, "HR_Recip_Second_DRB3/4/5"],
                              data.loc[row, "HR_Recip_Second_DQ_Split"], DQ2,
                              data.loc[row, "HR_Recip_Second_DQA"])
                        del dq_options[0]
        elif dq_options[1] in options.get(DR1):
            print (dq_options[1], options.get(DR1))
            for rule in classII:
                print("Option 3: ", rule[0])
                if rule[0] == DR1 and rule[4] == DQ2:
                    data.loc[row, "HR_Recip_First_DR_Split"] = rule[1]
                    data.loc[row, "HR_Recip_First_DRB3/4/5"] = rule[3]
                    data.loc[row, "HR_Recip_Second_DQ_Split"] = rule[5]
                    data.loc[row, "HR_Recip_Second_DQA"] = rule[6]
                    print('Option 3',DR1, data.loc[row, "HR_Recip_First_DR_Split"],
                          data.loc[row, "HR_Recip_First_DRB3/4/5"],
                          data.loc[row, "HR_Recip_Second_DQ_Split"], DQ2,
                          data.loc[row, "HR_Recip_Second_DQA"])
                    del dq_options[1]
                    print("Test2", dq_options)
                    break
            if dq_options[0] in options.get(DR2):
                for rule in classII:
                    print("Option 4: ", rule[0])
                    if rule[0] == DR2 and rule[4] == DQ1:
                        data.loc[row, "HR_Recip_Second_DR_Split"] = rule[1]
                        data.loc[row, "HR_Recip_Second_DRB3/4/5"] = rule[3]
                        data.loc[row, "HR_Recip_First_DQ_Split"] = rule[5]
                        data.loc[row, "HR_Recip_First_DQA"] = rule[6]
                        print('Option 4',DR2,
                              data.loc[row, "HR_Recip_Second_DR_Split"],
                              data.loc[row, "HR_Recip_Second_DRB3/4/5"],
                              data.loc[row, "HR_Recip_First_DQ_Split"], DQ1,
                              data.loc[row, "HR_Recip_First_DQA"])
                        del dq_options[0]



        # print (data.loc[[row]])

print(data)






