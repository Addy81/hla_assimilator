#!/usr/bin/python
#
#
#
#
# Adriana Toutoudaki (December 2018), contact: adriana.tou@gmail.com

import pandas as pd
import re
import sys
import numpy as np

# parse file into a variable
if len(sys.argv) == 1:
    sys.exit("Error: Please provide an input file.")

data_file = sys.argv[1]
print("File to be assimilated: %s " % data_file)

if len(sys.argv) == 2:
    output_file_name = str(data_file).replace(".xlsx", "_assimilated.xlsx")
    output_file = '../results/' + output_file_name
else:
    output_file = '../results/' + sys.argv[2]


rules_path = 'classII_rules.xlsx'
data = pd.read_excel(data_file, "Main data")
rows = data.shape[0]
rules = pd.read_excel('classII_rules.xlsx')

def fill_split(patient):
    """iterates through the columns containing the HLA data and
    fills the split column with the equivalent broad if empty"""

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
print ("Filling empty split column cells")
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

# Copy split column and rename it to with an HR_ prefix
for column in data.columns:
    column_check = re.search('_Split', column)
    col_index = data.columns.get_loc(column)
    new_column_name = "HR_" + column
    if column_check:
        data.insert((col_index + 1), new_column_name, data[column])

# when there's the first Cw present - assume homozygous so fill the Second Split column


def fill_hom(patient, gene):
    """Assuming when only one allele present it is homozygous
    so this function fills in the equivalent homozygous allele"""

    first = 'HR_' + patient + '_First_'+ gene + '_Split'
    second =  'HR_' + patient + '_Second_'+ gene + '_Split'

    for column in data.columns:
        f = re.match(second, column)
        if f:
            data[second] = data[second].fillna(data[first])
        else:
            pass

print("Filling missing homozygours alleles")
fill_hom('Recip', 'C')
fill_hom('Donor', 'C')
fill_hom('Recip', 'DQ')
fill_hom('Donor', 'DQ')

# Replace low-res alleles in the HR_ columns using the rule lists above
print("Assimilating Class I alleles")
for column in data.columns:
    column_check = re.match('HR_', column)
    if column_check:    
        data[column].replace(to_replace = A_LR, value = A_HR, inplace = True)
        data[column].replace(to_replace = B_LR, value = B_HR, inplace = True)
        data[column].replace(to_replace = C_LR, value = C_HR, inplace = True)
    else:
        pass


# special Cw/B pairing replacement
rows = data.shape[0]

def c_assimilation(to_replace, general_rule, exc1, exc2=(None, None),exc3=(None, None)):
    """replaces Cw alleles based on the B allele correlation"""

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


# Function that replaces Cw alleles based on the B allele correlation format of function is:
# to_replace - CwX : the low res allele to be substituted
# general_rule : C*xx:xx :the most common high-res allele
# exc1,exc2,exc3: tuple that contains the associated B allele with the special C to replace. (B*xx:xx,C*xx:xx)
c_assimilation(to_replace='Cw10', general_rule='C*03:02', exc1=('B*40:01', 'C*03:04'), exc2=('B*15:01', 'C*03:04'))
c_assimilation(to_replace='Cw8', general_rule='C*08:01', exc1=('B*14:01', 'C*08:02'), exc2=('B*14:02', 'C*08:02'))
c_assimilation(to_replace='Cw16', general_rule='C*16:01', exc1=('B*44:03', 'C*16:02'), exc2=('B*55:01', 'C*16:02'))
c_assimilation(to_replace='Cw7', general_rule='C*07:01', exc1=('B*07:02', 'C*07:02'))


#add a DR51/52/53 column
print ("Adding some extra columns.")
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

# create a list containing all class II rules
classII = []
rule_rows = rules.shape[0]
count = 1
for row in range(rule_rows):
    row_sublist = [count]
    count += 1
    for column in rules.columns:
        row_sublist.append(rules.loc[row][column])
    classII.append(row_sublist)

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

# Swap columns around to allow for the one with only one option to be first
print ("Assimilating Class II alleles.")
def column_swap(patient):
    for row in range(rows):
        count1 = 0
        count2 = 0
        DR1 = data.loc[row, "HR_" + patient + "_First_DR_Split"]
        DR2 = data.loc[row, "HR_" + patient + "_Second_DR_Split"]
        DQ1 = data.loc[row, "HR_" + patient + "_First_DQ_Split"]
        DQ2 = data.loc[row, "HR_" + patient + "_Second_DQ_Split"]

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
            data.loc[row, "HR_" + patient + "_First_DR_Split"] = DR2
            data.loc[row, "HR_" + patient + "_Second_DR_Split"] = DR1

column_swap("Recip")
column_swap("Donor")

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
add_sub_column("Donor")


dq_splits = ["DQ2","DQ4","DQ5","DQ6","DQ7","DQ8","DQ9"]
dr_splits = ["DR1","DR103","DR4","DR7","DR8","DR9","DR10","DR11","DR12","DR13","DR14","DR15","DR16","DR17","DR18"]
dq_broads = ["DQ1", "DQ3"]
dr_broads = ["DR5", "DR6", "DR2", "DR3"]

def assign_sub_codes(patient):
    """function that matches DR-DQs and assigns a code to be then substituted"""

    with open((patient + "_classII_log.txt"), "w+") as f:

        for row in range(rows):
            R1 = data.loc[row, ("HR_" + patient + "_First_DR_Split")]
            R2 = data.loc[row, "HR_" + patient + "_Second_DR_Split"]
            Q1 = data.loc[row, "HR_" + patient + "_First_DQ_Split"]
            Q2 = data.loc[row, "HR_" + patient + "_Second_DQ_Split"]
            first_sub = patient + "_First_Sub"
            second_sub = patient + "_Second_Sub"
            printed_options = str(R1) + "," + str(R2) + "," + str(Q1) + "," + str(Q2)

            if (type(R1) != str) or (type(R2) != str):
                f.write("%d: DR alleles missing --> %s\n" % (row, printed_options))
                continue
            elif (R1 not in dr_splits) or (R2 not in dr_splits):
                f.write("%d: DR alleles splits are missing --> %s\n" % (row, printed_options))
                continue
            else:
                if (type(Q1) != str) or (type(Q2) != str):
                    f.write("%d: DQ alleles missing --> %s\n" % (row, printed_options))
                    continue
                elif (Q1 not in dq_splits) or (Q2 not in dq_splits):
                    f.write("%d: DQ alleles splits are missing--> %s\n" % (row, printed_options))
                    continue
                else:
                    dq_options = [Q1, Q2]

                    while len(dq_options) > 0:
                        if dq_options[0] in options.get(R1):
                            for rule in classII:
                                if rule[1] == R1 and rule[5] == Q1:
                                    data.loc[row, first_sub] = "a" + str(rule[0])
                                    del dq_options[0]
                                    break
                            if dq_options[0] in options.get(R2):
                                for rule in classII:
                                    if rule[1] == R2 and rule[5] == Q2:
                                        data.loc[row, second_sub] = "a" + str(rule[0])
                                        del dq_options[0]
                            else:
                                f.write("%d: options dont work (1)--> %s\n" % (row, printed_options))
                                break
                        elif dq_options[1] in options.get(R1):
                            for rule in classII:
                                if rule[1] == R1 and rule[5] == Q2:
                                    data.loc[row, first_sub] = "b" + str(rule[0])
                                    del dq_options[1]
                                    break
                            if dq_options[0] in options.get(R2):
                                for rule in classII:
                                    if rule[1] == R2 and rule[5] == Q1:
                                        data.loc[row, second_sub] = "b" + str(rule[0])
                                        del dq_options[0]
                            else:
                                f.write("%d: options dont work (2)--> %s\n" % (row, printed_options))
                                break
                        else:
                            f.write("%d: options dont work (3)--> %s\n" % (row, printed_options))
                            break


assign_sub_codes("Recip")
assign_sub_codes("Donor")


def assimilate_classII(patient):
    """ Function that substitutes low-res with high-res class II alleles"""

    for row in range(rows):
        code1 = data.loc[row, patient + "_First_Sub"]
        code2 = data.loc[row, patient + "_Second_Sub"]
        R1 = data.loc[row, "HR_" + patient + "_First_DR_Split"]
        R2 = data.loc[row, "HR_" + patient + "_Second_DR_Split"]
        Q1 = data.loc[row, "HR_" + patient + "_First_DQ_Split"]
        Q2 = data.loc[row, "HR_" + patient + "_Second_DQ_Split"]
        #print(code1,code2)

        if type(code1) != str or type(code2) != str:
            continue
        elif code1.startswith("a"):
            code1 = int(code1.lstrip("a"))
            code2 = int(code2.lstrip("a"))
            for rule in classII:
                if rule[0] == code1:
                    data.loc[row, "HR_" + patient + "_First_DR_Split"] = rule[2]
                    data.loc[row, "HR_" + patient + "_First_DRB3/4/5"] = rule[4]
                    data.loc[row, "HR_" + patient + "_First_DQ_Split"] = rule[6]
                    data.loc[row, "HR_" + patient + "_First_DQA"] = rule[7]
                if rule[0] == code2:
                    data.loc[row, "HR_" + patient + "_Second_DR_Split"] = rule[2]
                    data.loc[row, "HR_" + patient + "_Second_DRB3/4/5"] = rule[4]
                    data.loc[row, "HR_" + patient + "_Second_DQ_Split"] = rule[6]
                    data.loc[row, "HR_" + patient + "_Second_DQA"] = rule[7]
        elif code1.startswith("b"):
            code1 = int(code1.lstrip("b"))
            code2 = int(code2.lstrip("b"))
            for rule in classII:
                if rule[0] == code1:
                    data.loc[row, "HR_" + patient + "_First_DR_Split"] = rule[2]
                    data.loc[row, "HR_" + patient + "_First_DRB3/4/5"] = rule[4]
                    data.loc[row, "HR_" + patient + "_Second_DQ_Split"] = rule[6]
                    data.loc[row, "HR_" + patient + "_Second_DQA"] = rule[7]
                if rule[0] == code2:
                    data.loc[row, "HR_" + patient + "_Second_DR_Split"] = rule[2]
                    data.loc[row, "HR_" + patient + "_Second_DRB3/4/5"] = rule[4]
                    data.loc[row, "HR_" + patient + "_First_DQ_Split"] = rule[6]
                    data.loc[row, "HR_" + patient + "_First_DQA"] = rule[7]


assimilate_classII("Recip")
assimilate_classII("Donor")

print("Tidying up your file.\n")
data.drop(columns= ['Recip_First_Sub', 'Recip_Second_Sub', 'Donor_First_Sub', 'Donor_Second_Sub'])

# save file into a different excel file

print("Writing your assimilated alleles in a brand new excel file.\n")
writer = pd.ExcelWriter(output_file, engine = 'xlsxwriter')

data.to_excel(writer,sheet_name='Main data')
writer.save()

print("Success! Your new file %s is ready to view" % output_file_name)
