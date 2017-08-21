from Bio import SeqIO
import pandas as pd
import json
import re
from modules.PanPredic.definitions import ROOT_DIR
import pdb
import sys 

import os
from modules.PanPredic.pan_utils import get_URIs



def cmd_parse_pan(file):
    
    """
    Drops all columns except genome name and presence or abscence vector -> only used to build model for ML
    :param :
        A tab delimited csv file from a panseq output
    :return: 
       a file with reduced headers and the NA's dropped
    """

    df = pd.read_csv(file, sep=None)
    #drop columns we don't need
    df = df.drop(['LocusName', 'Start Bp', 'End Bp', 'Contig'], axis=1)

    df = df.drop_duplicates(subset=['LocusID', 'Genome'], keep='first')

    #drop rows we don't need
    
    df.to_csv(ROOT_DIR + '/tests/data/genparsed.txt', mode='w+', header=False, index=False, sep = '\t')
    
    return ROOT_DIR + '/tests/data/genparsed.txt'

def pred_parse_pan(file):
    
    """
    Drops all columns except genome name and presence or abscence vector -> only used to build model for ML
    :param :
        A tab delimited csv file from a panseq output
    :return: 
       a file with reduced headers and the NA's dropped
    """
    #the file size is too big to read in all at once
    chunksize = 10 ** 6
    for chunk in pd.read_csv(file, sep=None, chunksize=chunksize):
    #drop columns we don't need
        chunk = chunk.drop(['LocusName', 'Start Bp', 'End Bp', 'Contig'], axis=1)
    #drop rows we don't need
        chunk.to_csv(ROOT_DIR + '/tests/data/genparsed.txt', mode='a', header=False, index=False, sep = '\t')

    return ROOT_DIR + '/tests/data/genparsed.txt'


def pred_categorizer(file):
    """
     
    :param:
        A tab delim file that has only two columns, genomename and a 1 for presence and 0 for abscence
    :return: 
        A dict that only needs {genome : {values: [0, 1, 0, 1, 0, 0 ............]}, .........}
    """
    df = pd.read_csv(file, sep='\t', header=None)

    os.remove(file)
    

    genome_dict = {}
    pangenome = []
    for row in df.iterrows():

        index, data = row
        pan_list = data.tolist()

        value = pan_list[2]
        genome = pan_list[1]
        region = pan_list[0]

        if genome in genome_dict:
            genome_dict[genome][region] = value

        else:
            genome_dict[genome] = {region : value}
              
    return genome_dict


def categorizer(file):
    """
     
    :param:
        A tab delim file that has only two columns, genomename and a 1 for presence and 0 for abscence
    :return: 
        A dict that only needs {genome : {values: [0, 1, 0, 1, 0, 0 ............]}, .........}
    """
    df = pd.read_csv(file, sep='\t', header=None)

    os.remove(file)
    

    genome_dict = {}
    pangenome = []
    for row in df.iterrows():


        index, data = row
        pan_list = data.tolist()

        value = pan_list[2]
        genome = pan_list[1]
  
        if genome in genome_dict:
            genome_dict[genome]['values'].append(value)

        else:
            genome_dict[genome] = {'values': []}
            genome_dict[genome]['values'].append(value)
              
    return genome_dict

def get_pan_order():

    old_pan = ROOT_DIR + '/tests/data/panResults2/pan_genome.txt'

    #the file size is too big to read in all at once

    df = pd.read_csv(old_pan, sep=None)
    #drop columns we don't need
    print(df.count())
    df = df.drop(['LocusName', 'Allele', 'Start Bp', 'End Bp', 'Contig'], axis=1)
    print(df.count())
    dflist = df['LocusID'].values.tolist()
    print ('length of array')
    print(len(dflist))
    i = 0
    genome_count = 0
    prev = 'abc'

    genome_set = 0
    actual_set = 0
    list1 = []
    list2 = []
    '''
    for region in dflist:
        if region not in list1:
            list1.append(region)
        else:
            if region != prev:
                if region == 'ed817b45f3b7dd143b0431992131021e9e06ad35':
                    print 'THE INNER LOOP'
                    print actual_set
                print(region)
        actual_set = actual_set + 1
        genome_count = genome_count + 1
        if region != prev:
            list2.append(region)
            i = i + 1
            genome_set = genome_set + 185
            if genome_count < 185:
                print('not enough genomes')
                print genome_count
                print region
            genome_count = 0
        prev = region
    '''
    df = df.drop_duplicates(subset=['LocusID'], keep='first')
    unique_list = df.LocusID.unique()
    print(len(unique_list))
    print(df.count())
    list = df['LocusID'].values.tolist()
    print(len(list))

    return list

def get_vector_order(dict, list):

    ordered_dict = {}

    for genome in dict:
        ordered_dict[genome] = {'values' : []}

        for region in list:
            if region in dict[genome]:
                ordered_dict[genome]['values'].append(dict[genome][region])
            else:
                ordered_dict[genome]['values'].append(0)


    return ordered_dict
            

def cmd_workflow(pan_file):

    parsed_file = cmd_parse_pan(pan_file)
    pan_dict = categorizer(parsed_file)

    return pan_dict


def pred_workflow(pan_file):

    parsed_file = pred_parse_pan(pan_file)
    dict = pred_categorizer(parsed_file)
    list = get_pan_order()
    print(len(list))

    ordered_dict = get_vector_order(dict, list)

    return ordered_dict
    
#get_pan_order()
#cmd_workflow('/home/james/backend/app/modules/PanPredic/tests/data/panResults2/pan_genome.txt')
