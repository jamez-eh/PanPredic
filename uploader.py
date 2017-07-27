from Bio import SeqIO
import pandas as pd
import json
import re
from modules.PanPredic.definitions import ROOT_DIR

import sys 

import os
from modules.PanPredic.pan_utils import get_URIs

import pickle

from modules.PanPredic.pan_utils import contig_name_parse
from hashlib import sha1

'''
def contig_name_parse(pan_contig):
    """
    The panseq contig name is unhelpful
    :param:
        a contig named by panseq
    :return: 
        the basename of the contig
    """
    pan_contig = re.sub('[|]', '', pan_contig)

    if re.search('(.*?)(?=_E)', pan_contig):
        #m = re.search('(?<=\|)(.*?)(?=_E)', pan_contig)
        m = re.search('(.*?)(?=_E)', pan_contig)
        #m = re.search('(?<=\|).+', m.group(0))

    #elif re.search('(?<=\|).+', pan_contig):
        #m = re.search('(?<=\|).+', pan_contig)
        #m = re.search('(?<=\|).+', m.group(0))

    else:
        return pan_contig

    return m.group(0)
'''



#drop rows with no value and drop columns we don't need
def parse_pan(file):
    """
    :param :
        A tab delimited csv file from a panseq output
    :return: 
       a file with reduced headers and the NA's dropped
    """
    #the file size is too big to read in all at once
    chunksize = 10 ** 6
    for chunk in pd.read_csv(file, sep=None, chunksize=chunksize):
    #drop columns we don't need
        chunk = chunk.drop(['LocusName', 'Allele'], axis=1)
    #drop rows we don't need
        chunk = chunk.dropna(axis=0, how='any')

        chunk.to_csv(ROOT_DIR + '/tests/data/genparsed.txt', mode='a', header=False, index=False, sep = '\t')

    return ROOT_DIR + '/tests/data/genparsed.txt'

def pickler(file, query_files):
    '''
    This is creates a pickle to pass to the front end.............. (which we aren't doing)
    '''
    df = pd.read_csv(file, sep=None)
    os.remove(file)


    region_list = []

    for row in df.iterrows():
        index, data = row
        pan_list = data.tolist()
        row_dict = {}

        # the variable gene name here is just so that the module will work within superphy (datastruct_savvy)
        # The 'GENE_NAME' actually refers to the Locus Name and should be renamed to reflect this



        row_dict['hitname'] = str(pan_list[0])
        row_dict['filename'] = pan_list[1]

        row_dict['hitstart'] = pan_list[2]
        row_dict['hitstop'] = pan_list[3]
        row_dict['hitcutoff'] = 90
        row_dict['hitorientation'] = 'N/A'
        row_dict['analysis'] = 'Panseq'

        # parse name to accession number
        row_dict['contigid'] = contig_name_parse(pan_list[4])

        region_list.append(row_dict)

    pickle_file = query_files + '/panseq.p'
    pickle.dump(region_list, open(pickle_file, 'wb'))


    return pickle_file


# turn a datafarame to a list of rows lists
def pan_to_dict(file, hash_dict):
    """
     
    :param:
        A pandas dataframe from panseq
    :return: 

        A dictionary in the format for superphy to accept to add to blazegraph 
        ex. {'Some_Contig_ID':[{'START','STOP','ORIENTATION','GENE_NAME'}, {}, ....], etc}
    """
    df = pd.read_csv(file, sep=None)
    #don't remove the file if pickle is going to be called in workflow
    #os.remove(file)

    # used to check if there is a reference pangenome being checked with queryfile, we do this because otherwise we end up giving pangenome regions already in blazegraph new names
    '''
    previous_pan = False
    if query_panseq(): 
        previous_pan = True
    '''
    genome_dict = {}

    for row in df.iterrows():
        index, data = row
        pan_list = data.tolist()
        row_dict = {}

        # the variable gene name here is just so that the module will work within superphy (datastruct_savvy)
        # The 'GENE_NAME' actually refers to the Locus Name and should be renamed to reflect this


        # Because of how panseq names outputs we have an optional parse here, that if there is a queryfile for a previous pangenome then we must take the locusID from the locusName in pan_genome.txt
        '''
        if previous_pan:
            row_dict['GENE_NAME'] = resolve_locus(pan_list[1])
        else:

        '''
        row_dict['GENE_NAME'] = str(pan_list[0])

        row_dict['START'] = pan_list[2]
        row_dict['STOP'] = pan_list[3]

        # parse name to accession number
        contig_name = contig_name_parse(pan_list[4])

        genome = pan_list[1]

        # replace genome name with genome URI
        if genome in hash_dict:
            genome = hash_dict[genome]

        if genome in genome_dict:

            if contig_name in genome_dict[genome]:
                genome_dict[genome][contig_name].append(row_dict)

            else:
                genome_dict[genome][contig_name] = [row_dict]
        else:
            genome_dict[genome] = {contig_name: []}
            genome_dict[genome][contig_name] = [row_dict]

    return genome_dict

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
    df = pd.read_csv(file, sep=None)
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
    return genome_dict


def get_sequence_dict(file):
    """
    :param:
        a fasta file
    :return: 
        A dictionary in the format {header:sequence, header:sequence, ....}
    """

    sequence_dict = {}
    for record in SeqIO.parse(file, "fasta"):
        sequence_dict[record.description] = str(record.seq)
    return sequence_dict

#TODO: refactor this code so it is faster
#merges sequence data for storage in blazegraph
#THIS COULD BE WHERE THE PROBLEM IS!

def merge_dicts(pan_dict, seq_dict):
    number = 0
    for genome in pan_dict:
        for contig in pan_dict[genome]:
            for panregion in pan_dict[genome][contig]:
                for header in seq_dict:
                    if header == panregion['GENE_NAME']:
                        panregion['DNASequence'] = seq_dict[header]
                        #panregion['GENE_NAME'] = str(sha1(seq_dict[header].encode()).hexdigest())
                        break
    return {'PanGenomeRegion': pan_dict}


def json_dump(file, dict):
    with open(file, 'w') as fp:
        json.dump(dict, fp)


def json_load(file):
    with open(file) as fp:
        data = json.load(fp)

    return data



#generates a hash for a file
def generate_hash(filename):

    """
    :param:
        a file 
    :return: 
        sha1 hash
    """


    # the 'b' isn't needed less you run this on Windows
    with open(filename, 'rb') as f:
    #  we apply a sort func to make sure the contents are the same,        # regardless of order
        return sha1(str(sorted(f.readlines())).encode('utf-8')).hexdigest()




#replaces contig names from panseq with those compatible with blazegraph
def hash_merge(hash_dict, pan_dict):

    for contig in pan_dict:
        pan_dict[hash_dict[contig]] = pan_dict[contig]
        del pan_dict[contig]

    return pan_dict



#parses the locus name for the locusId when we are adding additional pan genome regions to the db
def resolve_locus(locus):

    if re.search('(?<=phy_)(.*?)(?=_\()', locus):
        m = re.search('(?<=phy_)(.*?)(?=_\()', locus)
        return m.group(0)

    else:
        return locus

def workflow(pan_file, seq_file, query_files):


    hash_dict = get_URIs(query_files)
    parsed_file = parse_pan(pan_file)
    pan_dict = pan_to_dict(parsed_file, hash_dict)

    #make a pickle for the front end (beautify)
    #pickle = pickler(parsed_file, query_files)

    seq_dict = get_sequence_dict(seq_file)
    final_dict = merge_dicts(pan_dict, seq_dict)

    return final_dict


def cmd_workflow(pan_file):

    parsed_file = cmd_parse_pan(pan_file)
    pan_dict = categorizer(parsed_file)

    return pan_dict
