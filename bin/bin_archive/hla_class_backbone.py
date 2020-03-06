#!/usr/bin/python3
#
#
#
#
# Adriana Toutoudaki (January 2019), contact: adriana.tou@gmail.com

import pandas as pd
import re
import sys
import os.path
import numpy as np
import csv
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser( description='Assimilate low resolution HLA type data.')
    parser.add_argument('input', help='Input excel .xlsx to be analysed')
    parser.add_argument('-o','--output', help='Desired output name filename to be ')
    arguments = parser.parse_args()

    return arguments

class Spreadsheet:

    def __init__(self, xlpath, projdir):
        """Initialize parent class."""
        self.xlpath = xlpath
        self.projdir = projdir
        if os.path.exists(xlpath):
            self.ws = pd.read_excel(xlpath, "Main data")
        else:
            raise FileNotFoundError(
                    "File not found: " + xlpath)

        # strip trailing whitespace
        self.ws.columns = map(str.rstrip, self.ws.columns)

    def create_df(self):

        return self.ws


class Patient:

    def __init__(self, id, patient_type, tx_id):
        self.id = id
        self.patient_type = patient_type
        self.tx_id = tx_id

    def make_identifier(self):

        patient_id = ':'.join([self.patient_type, str(self.id), 'TX', str(self.tx_id)])
        return patient_id


class Allele:

    def __init__(self,patient, gene,broads=[], splits=[]):
        self.gene = gene
        self.broads = broads
        self.splits = splits
        self.patient = patient
        self.high_res = []

    def show_info(self):
        print(self.patient)
        print(self.broads,type(self.broads[0]),type(self.broads[1]))
        print(self.splits,type(self.splits[0]),type(self.splits[1]))

    def fill_split(self):
        if isinstance(self.splits[0],float):
            self.splits[0] = self.broads[0]
        if isinstance(self.splits[1],float):
            self.splits[1] = self.broads[1]

    def fill_hom(self):
        if isinstance(self.splits[1],float):
            self.splits[1] = self.splits[0]


    def assimilate(self):
        # hard-coded list of rules. This can be parsed to the script instead if preferred.
        A_rules = {
            'A1': 'A*01:01', 'A2': 'A*02:01', 'A3': 'A*03:01', 'A11': 'A*11:01', 'A23': 'A*23:01', 'A24': 'A*24:02',
         'A25': 'A*25:01', 'A26': 'A*26:01', 'A29': 'A*29:02', 'A30': 'A*30:01', 'A31': 'A*31:01', 'A32': 'A*32:01',
         'A33': 'A*33:01', 'A34': 'A*34:01', 'A36': 'A*36:01', 'A43': 'A*43:01', 'A66': 'A*66:01', 'A68': 'A*68:01',
         'A69': 'A*69:01', 'A74': 'A*74:01', 'A80': 'A*80:01'
        }
        B_rules = {
            'B7': 'B*07:02', 'B8': 'B*08:01', 'B13': 'B*13:01', 'B64': 'B*14:01', 'B65': 'B*14:02', 'B62': 'B*15:01',
         'B75': 'B*15:02', 'B72': 'B*15:03', 'B71': 'B*15:10', 'B76': 'B*15:12', 'B77': 'B*15:13', 'B63': 'B*15:16',
         'B18': 'B*18:01', 'B27': 'B*27:05', 'B35': 'B*35:01', 'B37': 'B*37:01', 'B38': 'B*38:01', 'B39': 'B*39:01',
         'B60': 'B*40:01', 'B61': 'B*40:02', 'B40': 'B*40:05', 'B41': 'B*41:01', 'B42': 'B*42:01', 'B44': 'B*44:02',
         'B45': 'B*45:01', 'B46': 'B*46:01', 'B47': 'B*47:01', 'B48': 'B*48:01', 'B49': 'B*49:01', 'B50': 'B*50:01',
         'B51': 'B*51:01', 'B52': 'B*52:01', 'B53': 'B*53:01', 'B54': 'B*54:01', 'B55': 'B*55:01', 'B56': 'B*56:01',
         'B57': 'B*57:01', 'B58': 'B*58:01', 'B59': 'B*59:01', 'B67': 'B*67:01', 'B73': 'B*73:01', 'B78': 'B*78:01',
         'B81': 'B*81:01', 'B82': 'B*82:01'
        }
        C_rules = {
            'Cw1': 'C*01:02', 'Cw2': 'C*02:02', 'Cw4': 'C*04:01', 'Cw9': 'C*03:03', 'Cw5': 'C*05:01', 'Cw6': 'C*06:02',
         'Cw12': 'C*12:03', 'Cw14': 'C*14:02', 'Cw15': 'C*15:02', 'Cw17': 'C*17:01', 'Cw18': 'C*18:01'
        }

        if self.gene == 'A':
            for lr_allele in self.splits:
                if lr_allele in list(A_rules.keys()):
                    self.high_res.append(A_rules[lr_allele])

    def print_allele_information(self):
        print(self.patient)
        print(self.splits)
        print(self.high_res)


class SpecialAllele(Allele):
    pass


def make_patient_lists(df):
    Recipients = []
    Donors = []

    for row in df.create_df().itertuples():
        recipient_instance = Patient(row.RECIP_ID, 'R', row.TX_ID)
        donor_instance = Patient(row.DONOR_ID, 'D', row.TX_ID)
        Recipients.append(recipient_instance.make_identifier())
        Donors.append(donor_instance.make_identifier())

    return (Recipients,Donors)


def extract_information(df):

    for row in df.create_df().itertuples():
        recipient_instance = Patient(row.RECIP_ID, 'R', row.TX_ID)
        donor_instance = Patient(row.DONOR_ID, 'D', row.TX_ID)

        recip_allele = Allele(recipient_instance.make_identifier(),'A',[row.Recip_First_A_Broad,row.Recip_Second_A_Broad],
                     [row.Recip_First_A_Split,row.Recip_Second_A_Split])
        donor_allele = Allele(donor_instance.make_identifier(),'A',[row.Donor_First_A_Broad,row.Donor_Second_A_Broad],

                     [row.Donor_First_A_Split,row.Donor_Second_A_Split])

    return recip_allele,donor_allele

def update_allele(allele):
    allele.fill_split()
    allele.fill_hom()
    allele.assimilate()
    allele.print_allele_information()


def main(args):

    data = Spreadsheet(args.input,'/mnt/storage/home/toutoua/projects/tt')
    #print(data.create_df())

    Recipients,Donors=make_patient_lists(data)

    recip_allele,donor_allele = extract_information(data)
    update_allele(recip_allele)
    update_allele(donor_allele)




if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments)
