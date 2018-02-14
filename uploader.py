from Bio import SeqIO
import pandas as pd
import json
import re
from modules.PanPredic.definitions import ROOT_DIR
import sys

import os
from modules.PanPredic.pan_utils import get_URIs
from middleware.graphers.turtle_utils import slugify
import pickle

from modules.PanPredic.pan_utils import contig_name_parse
from hashlib import sha1




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


def genome_replace(hash_dict, genome):
    for entry in hash_dict:
        if re.search((genome), entry):
            return hash_dict[entry]
    return genome



# turn a datafarame to a list of rows lists
def pan_to_dict(file, hash_dict):
    """

    :param:
        A pandas dataframe from panseq
    :return:

        A dictionary in the format for superphy to accept to add to blazegraph
        ex. {'Some_Contig_ID':[{'START','STOP','ORIENTATION','GENE_NAME'}, {}, ....], etc}
    """
    df = pd.read_csv(file, sep=None, header=None)
    #don't remove the file if pickle is going to be called in workflow
    os.remove(file)



    genome_dict = {}

    for row in df.iterrows():
        index, data = row
        pan_list = data.tolist()
        row_dict = {}

        # the variable gene name here is just so that the module will work within superphy (datastruct_savvy)
        # The 'GENE_NAME' actually refers to the Locus Name and should be renamed to reflect this


        # Because of how panseq names outputs we have an optional parse here, that if there is a queryfile for a previous pangenome then we must take the locusID from the locusName in pan_genome.txt

        row_dict['GENE_NAME'] = str(pan_list[0])

        row_dict['START'] = pan_list[2]
        row_dict['STOP'] = pan_list[3]

        # parse name to accession number
        contig_name = contig_name_parse(pan_list[4])

        genome = pan_list[1]
        genome = genome_replace(hash_dict, genome)

        if genome in genome_dict:

            if contig_name in genome_dict[genome]:
                genome_dict[genome][contig_name].append(row_dict)

            else:
                genome_dict[genome][contig_name] = [row_dict]
        else:
            genome_dict[genome] = {contig_name: []}
            genome_dict[genome][contig_name] = [row_dict]

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






#parses the locus name for the locusId when we are adding additional pan genome regions to the db
def resolve_locus(locus):

    if re.search('(?<=phy_)(.*?)(?=_\()', locus):
        m = re.search('(?<=phy_)(.*?)(?=_\()', locus)
        return m.group(0)

    else:
        return locus

def workflow(pan_file, seq_file, query_files):
    '''
    param: pan_file: pan_genome.txt
    param: seq_file : accessorygenome.fasta
    param: query_files: dir with sequences that generated the pangenome
    '''

    #get a dict of genome_name:file hash
    hash_dict = get_URIs(query_files)


    parsed_file = parse_pan(pan_file)

    pan_dict = pan_to_dict(parsed_file, hash_dict)

    #replace genome names with file hashes



    #make a pickle for the front end (beautify)
    #pickle = pickler(parsed_file, query_files)

    seq_dict = get_sequence_dict(seq_file)
    final_dict = merge_dicts(pan_dict, seq_dict)

    return final_dict
