
from Bio import SeqIO
from os.path import basename
import os
import sys
import pandas as pd
import json
import re
from definitions import ROOT_DIR




def contig_name_parse(pan_contig):
    """
    The panseq contig name is unhelpful
    :param:
        a contig named by panseq
    :return: 
        the basename of the contig
    """

    if re.search('(?<=\|)(.*?)(?=_E)', pan_contig):
        m = re.search('(?<=\|)(.*?)(?=_E)', pan_contig)
        m = re.search('(?<=\|).+', m.group(0))

    else:
        m = re.search('(?<=\|).+', pan_contig)
        m = re.search('(?<=\|).+', m.group(0))

    return m.group(0)




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


#turn a datafarame to a list of rows lists
def pan_to_dict(file):

    """
    :param:
        A pandas dataframe from panseq
    :return: 
        A dictionary in the format for superphy to accept to add to blazegraph 
        ex. {'Some_Contig_ID':[{'START','STOP','ORIENTATION','GENE_NAME'}, {}, ....], etc}
    """
    df = pd.read_csv(file, sep=None)
    #os.remove(file)

    i = 0
    prev_ID = None
    pan_dict = {}
    for row in df.iterrows():
        index, data = row
        pan_list = data.tolist()
        row_dict = {}

        entry_list = []

        if prev_ID != pan_list[0]:
            prev_ID = pan_list[0]
            i = i + 1

        #the variable gene name here is just so that the module will work within superphy (datastruct_savvy)
        #The 'GENE_NAME' actually refers to the Locus Name and should be renamed to reflect this

        row_dict['GENE_NAME'] = pan_list[0]
        row_dict['GENOME'] = pan_list[1]
        row_dict['START'] = pan_list[2]
        row_dict['STOP'] = pan_list[3]
        contig_name = contig_name_parse(pan_list[4])

        if contig_name in pan_dict:
            pan_dict[contig_name].append(row_dict)

        else:
            pan_dict[contig_name] = [row_dict]

    return pan_dict


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

#merges sequence data for storage in blazegraph
def merge_dicts(pan_dict):

    for record in pan_dict:
        for panregion in pan_dict[record]:
            pan = "1496178616000"
            if pan in panregion.values():
                panregion['DNAseq'] = 'CTGA'
            print(panregion)


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

    from hashlib import sha1
    # the 'b' isn't needed less you run this on Windows
    with open(filename, 'rb') as f:
    #  we apply a sort func to make sure the contents are the same,        # regardless of order
        return sha1(str(sorted(f.readlines())).encode('utf-8')).hexdigest()


def main(dr):

    """
    :param:
        directory of fasta files
    :return: 
        Dictionary in format {contig_name: sha1hash} for each contig in fasta files
    """

    from Bio import SeqIO
    d = {}
    for f in os.listdir(dr):
        h = generate_hash(dr + f)
        for record in SeqIO.parse(open(dr + f), "fasta"):
            contig_name = contig_name_parse(record.id)
            d[contig_name] = '<https://www.github.com/superphy#' + h + '/contigs/' + contig_name + '>'
    json_dump('hash_dict.json', d)


#replaces contig names from panseq with those compatible with blazegraph
def hash_merge(hash_dict, pan_dict):
    for contig in pan_dict:
        print(contig)
        pan_dict[hash_dict[contig]] = pan_dict[contig]
        del pan_dict[contig]

    json_dump('merged.json', pan_dict)


main('/home/james/PanPredic/tests/data/filteredgenomes/')


hash_dict = json_load('/home/james/PanPredic/modules/hash_dict.json')

hash_merge(hash_dict,)

'''
gd = app.modules.turtleGrapher.turtle_grapher.generate_turtle_skeleton(sys.argv[1])
data = gd.serialize(format="turtle")
print(data)
'''

def workflow(pan_file, seq_file):

    parsed_file = parse_pan(pan_file)
    pan_dict = pan_to_dict(parsed_file)
    seq_dict = get_sequence_dict(seq_file)
    final_dict = merge_dicts(pan_dict, seq_dict)
    #results_dict = hash_merge()

    return final_dict


    #json_dump('pandump.json', pan_dict)