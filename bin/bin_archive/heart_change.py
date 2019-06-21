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
    data = pd.read_excel(data_file)

    return data

def rename_columns(data):

    original_columns = [ ' HLA-A* (R1)', ' HLA-A* (R2)',' HLA-B* (R1)', ' HLA-B* (R2)',' HLA-C* (R1)',' HLA-C* (R2)',' HLA-DR (R1)',' HLA-DR (R2)',' HLA-DQ (R1)',' HLA-DQ (R2)',' HLA-A* (D1)', ' HLA-A* (D2)',' HLA-B* (D1)', ' HLA-B* (D2)',' HLA-C* (D1)',' HLA-C* (D2)',' HLA-DR (D1)',' HLA-DR (D2)',' HLA-DQ (D1)',' HLA-DQ (D2)']

    desired_columns = ['Recip_First_A_Split','Recip_Second_A_Split','Recip_First_B_Split','Recip_Second_B_Split','Recip_First_C_Split','Recip_Second_C_Split','Recip_First_DR_Split','Recip_Second_DR_Split','Recip_First_DQ_Split','Recip_Second_DQ_Split','Donor_First_A_Split','Donor_Second_A_Split','Donor_First_B_Split','Donor_Second_B_Split','Donor_First_C_Split','Donor_Second_C_Split','Donor_First_DR_Split','Donor_Second_DR_Split','Donor_First_DQ_Split','Donor_Second_DQ_Split']

    column_dict = {}

    for num in range(0,20):
        column_dict[original_columns[num]] = desired_columns[num]

    data.rename(index = str,columns = column_dict, inplace = True)

    return data

def fill_donor_columns(data):
    donor_cols = ['Donor_First_A_Split','Donor_Second_A_Split','Donor_First_B_Split','Donor_Second_B_Split','Donor_First_C_Split','Donor_Second_C_Split']
    donor_original = [' HLA-A (D1)', ' HLA-A (D2)',' HLA-B (D1)', ' HLA-B (D2)',' HLA-C (D1)',' HLA-C (D2)']
    

    column_dict = {}

    for num in range(0,6):
        column_dict[donor_cols[num]] = donor_original[num]

    for column in data.columns:
        for pattern in donor_cols:
            if re.match(pattern,column):
                col_to_fill = column_dict[pattern]
                data[pattern] = data[pattern].fillna(data[col_to_fill])

    num_rows = data.shape[0]

    for column in donor_cols:
        col_index = data.columns.get_loc(column)

        for row in range(num_rows):
            cell = data.iloc[row][column]
            cell = str(cell).strip()

            if len(cell) == 4:
                data.iat[row,col_index] = cell[0]
            elif len(cell) > 4:
                data.iat[row,col_index] = cell[0:2]

def remove_dr_broads(data):

    columns = ['Donor_First_DR_Split','Donor_Second_DR_Split','Recip_First_DR_Split','Recip_Second_DR_Split']

    num_rows = data.shape[0]

    for column in columns:
        col_index = data.columns.get_loc(column)

        for row in range(num_rows):
            cell = data.iloc[row][column]
            cell = str(cell).strip()

            if len(cell) == 4:
                data.iat[row,col_index] = cell[0]
            elif len(cell) > 4:
                data.iat[row,col_index] = cell[0:2]



                

def remove_dq_broads(data):
    
    num_rows = data.shape[0]
    columns = ['Donor_First_DQ_Split','Donor_Second_DQ_Split','Recip_First_DQ_Split','Recip_Second_DQ_Split']

    for col in columns:
        col_index = data.columns.get_loc(col)

        for row in range(num_rows):
            cell = data.iloc[row][col]
            cell = str(cell).strip()
            if len(cell)>2:
                cell = 'DQ' + cell[0]
                data.iat[row,col_index] = cell
            elif cell == '-':
                data.iat[row,col_index] = ''
            elif cell =='nan':
                pass
            else:
                cell = 'DQ' + cell
                data.iat[row,col_index] = cell
    #return data


def alter_columns(data,gene):

    num_rows = data.shape[0]
    print (num_rows)
    column_patterns = ['Recip_First_', 'Recip_Second_', 'Donor_First_', 'Donor_Second_']

    for patt in column_patterns:
        column_to_change = patt + gene + '_Split'
        col_index = data.columns.get_loc(column_to_change)
        for row in range(num_rows):
            
            cell = data.iloc[row][column_to_change]

            cell = str(cell).strip()
            
            if cell == '02/92':
                data.iat[row,col_index] = 'A2'
            elif len(cell) > 3:
                cell = gene + '*' + cell
                data.iat[row,col_index] = cell
            elif cell.startswith('0'):
                cell = gene + cell[1]

                data.iat[row,col_index] = cell
                #print (row,data.loc[row,column_to_change])
            elif cell == 'nan':
                pass
                #print (data.loc[row,column_to_change])
                #print(cell)
            elif cell.startswith('-'):
                data.iat[row,col_index] = ''
                #print (data.loc[row,column_to_change])
            else:
                cell = gene + cell
                data.iat[row,col_index] = cell

                #print (data.loc[row,column_to_change])
                #print(row,cell, type(cell))
    return data
        

def change_c(data):
    num_rows = data.shape[0]
    columns = ['Donor_First_C_Split','Donor_Second_C_Split','Recip_First_C_Split','Recip_Second_C_Split']

    for col in columns:
        col_index = data.columns.get_loc(col)
    
        for row in range(num_rows):
            cell = data.iloc[row][col]
            cell = str(cell).strip()
            if cell.startswith('C'):
                cell = cell[0] + 'w' + cell[1:]
                data.iat[row,col_index] = cell




def main(args):

    dir_path = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(dir_path)
    data_path = os.path.join(parent,'data')
    log_path = os.path.join(data_path,'logs')
    data_file = args.input
    results = os.path.join(parent,'results')
    output = args.output
    
    if output is None:
        output_file_name = os.path.basename(data_file).replace(".xlsx", "_changed.xlsx")
    else:
        output_file_name = output
    
    output_file = os.path.join(data_path,output_file_name)

    data = parse_file(args)

    data = rename_columns(data)

    fill_donor_columns(data)

    remove_dr_broads(data)

    data = alter_columns(data,'A')
    data = alter_columns(data,'B')
    data = alter_columns(data,'C')
    data = alter_columns(data,'DR')
    #data = alter_columns(data,'DQ')


    remove_dq_broads(data)

    change_c(data)
    writer = pd.ExcelWriter(output_file, engine = 'xlsxwriter')

    data.to_excel(writer,sheet_name='Main data')
    writer.save()

    print("Success! Your new file %s is ready to view" % output_file_name)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
    