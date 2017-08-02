from Bio import SeqIO
import pandas as pd
import json
import re
from modules.PanPredic.definitions import ROOT_DIR

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
    #the file size is too big to read in all at once
    chunksize = 10 ** 6
    for chunk in pd.read_csv(file, sep=None, chunksize=chunksize):
    #drop columns we don't need
        chunk = chunk.drop(['LocusID', 'LocusName', 'Start Bp', 'End Bp', 'Contig'], axis=1)
    #drop rows we don't need
        chunk.to_csv(ROOT_DIR + '/tests/data/genparsed.txt', mode='a', header=False, index=False, sep = '\t')

    return ROOT_DIR + '/tests/data/genparsed.txt'


def categorizer(file):
    """
     
    :param:
        A tab delim file that has only two columns, genomename and a 1 for presence and 0 for abscence
    :return: 
        A dict that only needs {genome : {values: [0, 1, 0, 1, 0, 0 ............]}, .........}
    """
    df = pd.read_csv(file, sep=None, header=None)
    #don't remove the file if pickle is going to be called in workflow
    os.remove(file)
    

    genome_dict = {}
    pangenome = []
    for row in df.iterrows():

        index, data = row
        pan_list = data.tolist()

        value = pan_list[1]
        genome = pan_list[0]
  
        if genome in genome_dict:
            genome_dict[genome]['values'].append(value)

        else:
            genome_dict[genome] = {'values': []}
            genome_dict[genome]['values'].append(value)
        print(genome)
        print('length')
        print(len(genome_dict[genome]['values']))
              
    return genome_dict


def cmd_workflow(pan_file):

    parsed_file = cmd_parse_pan(pan_file)
    pan_dict = categorizer(parsed_file)

    return pan_dict



