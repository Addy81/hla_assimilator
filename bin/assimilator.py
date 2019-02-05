#!/usr/bin/python3
#
#
#
#
# Adriana Toutoudaki (January 2019), contact: adriana.tou@gmail.com

import pandas as pd
import re
import sys,os
import numpy as np
import csv
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser( description='Assimilate low resolution HLA type data.')
    parser.add_argument('input', help='Input excel .xlsx to be analysed')
    parser.add_argument('-o','--output', help='Desired output name filename to be ')
    arguments = parser.parse_args()

    return arguments

def parse_file(args):
    data_file = args.input
    data = pd.read_excel(data_file, "Main data")

    return data

def fill_split(data,patient):
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

def add_column(dtf,pattern):
    for column in dtf.columns:
        column_match = re.search(pattern,column)
        col_index = dtf.columns.get_loc(column)
        new_column_name = "HR_" + column
        if column_match: 
            dtf.insert((col_index + 1), new_column_name,dtf[column])
    

def fill_hom(data,patient, gene):
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

def assimilate_classI(dtf):
    # hard-coded list of rules. This can be parsed to the script instead if preferred.
    A_LR = ['A1', 'A2', 'A3', 'A11', 'A23', 'A24', 'A25', 'A26', 'A29', 'A30', 'A31', 'A32', 'A33', 'A34', 'A36', 'A43', 'A66', 'A68', 'A69', 'A74', 'A80']
    A_HR = ['A*01:01', 'A*02:01', 'A*03:01', 'A*11:01', 'A*23:01', 'A*24:02', 'A*25:01', 'A*26:01', 'A*29:02', 'A*30:01', 'A*31:01', 'A*32:01', 'A*33:01', 'A*34:01', 'A*36:01', 'A*43:01', 'A*66:01', 'A*68:01', 'A*69:01', 'A*74:01', 'A*80:01']
    B_LR = ['B7', 'B8', 'B13', 'B64', 'B65', 'B62', 'B75', 'B72', 'B71', 'B76', 'B77', 'B63', 'B18', 'B27', 'B35', 'B37', 'B38', 'B39', 'B60', 'B61', 'B40', 'B41', 'B42', 'B44', 'B45', 'B46', 'B47', 'B48', 'B49', 'B50', 'B51', 'B52', 'B53', 'B54', 'B55', 'B56', 'B57', 'B58', 'B59', 'B67', 'B73', 'B78', 'B81', 'B82']
    B_HR = ['B*07:02', 'B*08:01', 'B*13:01', 'B*14:01', 'B*14:02', 'B*15:01', 'B*15:02', 'B*15:03', 'B*15:10', 'B*15:12', 'B*15:13', 'B*15:16', 'B*18:01', 'B*27:05', 'B*35:01', 'B*37:01', 'B*38:01', 'B*39:01', 'B*40:01', 'B*40:02', 'B*40:05', 'B*41:01', 'B*42:01', 'B*44:02', 'B*45:01', 'B*46:01', 'B*47:01', 'B*48:01', 'B*49:01', 'B*50:01', 'B*51:01', 'B*52:01', 'B*53:01', 'B*54:01', 'B*55:01', 'B*56:01', 'B*57:01', 'B*58:01', 'B*59:01', 'B*67:01', 'B*73:01', 'B*78:01', 'B*81:01', 'B*82:01']
    C_LR = ["Cw1","Cw2","Cw4","Cw9","Cw5","Cw6","Cw12","Cw14","Cw15","Cw17","Cw18",]
    C_HR = ["C*01:02","C*02:02","C*04:01","C*03:03","C*05:01","C*06:02","C*12:03","C*14:02","C*15:02","C*17:01","C*18:01",]

    for column in dtf.columns:
        column_check = re.match('HR_', column)
        if column_check:
            dtf[column].replace(to_replace = A_LR, value = A_HR, inplace = True)
            dtf[column].replace(to_replace = B_LR, value = B_HR, inplace = True)
            dtf[column].replace(to_replace = C_LR, value = C_HR, inplace = True)
        else:
            pass

def c_assimilation(data,to_replace, general_rule, exc1, exc2=(None, None),exc3=(None, None)):
    """replaces Cw alleles based on the B allele correlation"""

    with open("classI_log.csv", "w+") as  classI:

        classI_log_writer = csv.writer(classI, delimiter = ' ', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        classI_log_writer.writerow(['Row', 'Reason', 'First', 'Second'])

        for patient in ['Recip', 'Donor']:
            for variable in ['First', 'Second']:
                rows = data.shape[0]
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
                        classI_log_writer.writerow([row, "C substituted with general rule", data.loc[row,c_col]])
                        data.loc[row, c_col] = re.sub(to_replace, general_rule, c)

def add_special_column (dtf,pattern,new_pattern):
    column_patterns = ['Recip_First', 'Recip_Second', 'Donor_First', 'Donor_Second']
    for c_pat in column_patterns:
        match_pattern = "HR_" + c_pat + pattern
        
        for column in dtf.columns:
            column_match =re.match(match_pattern,column)
            col_index= dtf.columns.get_loc(match_pattern)

            if column_match:
                new_column = "HR_" + c_pat + new_pattern
                dtf.insert((col_index+1),new_column,np.nan)

def create_rules(rules):
    classII = []
    rule_row_num = rules.shape[0]
    count = 1
    for row in range(rule_row_num):
        row_sublist = [count]
        count += 1
        for column in rules.columns:
            row_sublist.append(rules.loc[row][column])
        classII.append(row_sublist)
    
    return classII

def column_swap(data,options,patient):
    rows = data.shape[0]

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
    
def add_sub_column(data,patient):
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

def assign_sub_codes(data,options,log_path,patient,classII):
    """function that matches DR-DQs and assigns a code to be then substituted"""

    dq_splits = ["DQ2","DQ4","DQ5","DQ6","DQ7","DQ8","DQ9"]
    dr_splits = ["DR1","DR103","DR4","DR7","DR8","DR9","DR10","DR11","DR12","DR13","DR14","DR15","DR16","DR17","DR18"]
    dq_broads = ["DQ1", "DQ3"]
    dr_broads = ["DR5", "DR6", "DR2", "DR3"]
    rows = data.shape[0]

    
    with open((log_path + "/" + patient + "_classII_log.csv"), "w+") as log_file:
        log_writer = csv.writer(log_file,delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        log_writer.writerow(['Row','Reason','First_DR','Second_DR','First_DQ','Second_DQ'])

        for row in range(rows):
            R1 = data.loc[row, ("HR_" + patient + "_First_DR_Split")]
            R2 = data.loc[row, "HR_" + patient + "_Second_DR_Split"]
            Q1 = data.loc[row, "HR_" + patient + "_First_DQ_Split"]
            Q2 = data.loc[row, "HR_" + patient + "_Second_DQ_Split"]
            first_sub = patient + "_First_Sub"
            second_sub = patient + "_Second_Sub"
            printed_options = str(R1) + "," + str(R2) + "," + str(Q1) + "," + str(Q2)

            if (type(R1) != str) or (type(R2) != str):
                log_writer.writerow([row,'DR alleles missing', R1, R2, Q1,Q2])
                continue
            elif (R1 not in dr_splits) or (R2 not in dr_splits):
                log_writer.writerow([row, 'DR alleles splits are missing', R1, R2, Q1, Q2])
                continue
            else:
                if (type(Q1) != str) or (type(Q2) != str):
                    log_writer.writerow([row, 'DQ alleles missing', R1, R2, Q1, Q2])
                    continue
                elif (Q1 not in dq_splits) or (Q2 not in dq_splits):
                    log_writer.writerow([row, 'Dq alleles splits are missing', R1, R2, Q1, Q2])
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
                                log_writer.writerow([row, "Options don't work (1)", R1, R2, Q1, Q2])
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
                                log_writer.writerow([row, "Options don't work(2)", R1, R2, Q1, Q2])
                                break
                        else:
                            log_writer.writerow([row, "Options don't work(3)", R1, R2, Q1, Q2])
                            break

def assimilate_classII(data,patient,classII):
    """ Function that substitutes low-res with high-res class II alleles"""
    
    rows = data.shape[0]

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


def main(args):
    
    dir_path = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(dir_path)
    data_path = os.path.join(parent,'data')
    log_path = os.path.join(data_path,'logs')

    results = os.path.join(parent,'results')
    output = args.output
    
    if output is None:
        output_file_name = os.path.basename(data_file).replace(".xlsx", "_assimilated.xlsx")
    else:
        output_file_name = output
    
    output_file = os.path.join(data_path,output_file_name)
    
    data = parse_file(args)
    rows = data.shape[0]
    
    rules = pd.read_excel((data_path + '/classII_rules.xlsx'))
   
    # Run fill_split function for Recipient and Donor data
    print ("Filling empty split column cells")
    fill_split(data,'Recip')
    fill_split(data,'Donor')

   
    #Copies Split column and adds it next to the original with the prefix HR_ to be substituted
    add_column(data,'_Split')


    # when there's the first Cw present - assume homozygous so fill the Second Split column

    print("Filling missing homozygours alleles")
    fill_hom(data,'Recip', 'C')
    fill_hom(data,'Donor', 'C')
    fill_hom(data,'Recip', 'DQ')
    fill_hom(data,'Donor', 'DQ')
    
    # Replace low-res alleles in the HR_ columns using the rule lists above
    print("Assimilating Class I alleles")
    assimilate_classI(data)

    # special Cw/B pairing replacement
    rows = data.shape[0]
    # Function that replaces Cw alleles based on the B allele correlation format of function is:
    # to_replace - CwX : the low res allele to be substituted
    # general_rule : C*xx:xx :the most common high-res allele
    # exc1,exc2,exc3: tuple that contains the associated B allele with the special C to replace. (B*xx:xx,C*xx:xx)
    c_assimilation(data,to_replace='Cw10', general_rule='C*03:02', exc1=('B*40:01', 'C*03:04'), exc2=('B*15:01', 'C*03:04'))
    c_assimilation(data,to_replace='Cw8', general_rule='C*08:01', exc1=('B*14:01', 'C*08:02'), exc2=('B*14:02', 'C*08:02'))
    c_assimilation(data,to_replace='Cw16', general_rule='C*16:01', exc1=('B*44:03', 'C*16:02'), exc2=('B*55:01', 'C*16:02'))
    c_assimilation(data,to_replace='Cw7', general_rule='C*07:01', exc1=('B*07:02', 'C*07:02'))

    #add a DR51/52/53 and DQA column
    print ("Adding some extra columns.")

    add_special_column(data,'_DR_Split','_DRB3/4/5')     
    add_special_column(data,'_DQ_Split','_DQA')  
    
    # create a list containing all class II rules
    classII_rules = create_rules(rules)

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
    column_swap(data,options,"Recip")
    column_swap(data,options,"Donor")

    # USe it when we are back in normal dataset

    add_sub_column(data,"Recip")
    add_sub_column(data,"Donor")

    assign_sub_codes(data,options,log_path,"Recip",classII_rules)
    assign_sub_codes(data,options,log_path, "Donor",classII_rules)

    assimilate_classII(data,"Recip",classII_rules)
    assimilate_classII(data,"Donor",classII_rules)

    print("Tidying up your file.\n")
    data.drop(columns= ['Recip_First_Sub', 'Recip_Second_Sub', 'Donor_First_Sub', 'Donor_Second_Sub'])

    # save file into a different excel file

    print("Writing your assimilated alleles in a brand new excel file.\n")
    writer = pd.ExcelWriter(output_file, engine = 'xlsxwriter')

    data.to_excel(writer,sheet_name='Main data')
    writer.save()

    print("Success! Your new file %s is ready to view" % output_file_name)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
    