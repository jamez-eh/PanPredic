import pandas as pd
from app.modules.PanPredic.modules.uploader import parse_pan, json_load
from Bio import SeqIO
from app.modules.PanPredic.modules.queries import query_panseq, get_sequences
import re
from app.modules.PanPredic.modules.uploader import get_sequence_dict




def sequence_counter(file):
    """
    :param:
        a fasta file
    :return: 
        A dictionary in the format {header:sequence, header:sequence, ....}
    """
    i = 0

    for record in SeqIO.parse(file, "fasta"):
        i = i + 1
    return i

#parse_pan('/home/james/backend/app/modules/PanPredic/tests/data/panResults/pan_genome.txt')

def dict_counter (file):

    dict = json_load(file)

    genomes = 0
    contigs = 0
    pan_regions = 0

    for genome in dict:
        genomes = genomes + 1
        for contig in dict[genome]:
            contigs = contigs + 1
            for pan_region in dict[genome][contig]:
                pan_regions = pan_regions + 1

    print('genomes: ')
    print(genomes)
    print('contigs: ')
    print(contigs)
    print('PanGenomeRegions: ')
    print(pan_regions)

#dict_counter('/home/james/backend/app/modules/PanPredic/tests/data/pan_to_dict.json')


#makes a list of those in db that are not in our new file
def comparison (new_dict):
    count = 0
    found = True
    not_found = []
    current_pan = query_panseq()
    new_pan = json_load(new_dict)
    for panregion in current_pan:
        if found == False:
            not_found.append(panregion)
        found = False
        for genome in new_pan:
            for contig in new_pan[genome]:
                m = re.search('(?<=#).+', panregion)
                n = m.group(0)
                for pan in new_pan[genome][contig]:
                    if n == pan['GENE_NAME']:
                        count = count + 1
                        found = True
                        break

    print(count)
    print(not_found)


#comparison('/home/james/backend/app/modules/PanPredic/tests/data/merge_dicts.json')
#checks our output file for the same sequences in the db
def access_check():
    seq_dict = get_sequence_dict('/home/james/backend/app/modules/PanPredic/tests/data/panResults/accessoryGenomeFragments.fasta')
    sequence_count = 0
    match_count = 0
    #with open ('/home/james/backend/app/modules/PanPredic/tests/data/sequence_errors.fasta', 'a+') as f:
    for header in seq_dict:
        sequence_count = sequence_count + 1
        seq = seq_dict[header]
        if get_sequences(seq):
            match_count = match_count + 1
            print('SUCCESS')
        else:
            print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
            print('FAILURE')
            header = '>' + header + '\n'
            print(header)
            print(seq)
            #seq = seq + '\n'
            #f.write(header)
            #f.write(seq)
            print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')



    print(sequence_count)
    print(match_count)

def access_check2():
    seq_dict = get_sequence_dict('/home/james/backend/app/modules/PanPredic/tests/data/panResults/accessoryGenomeFragments.fasta')
    seq_dict2 = get_sequence_dict('/home/james/backend/app/modules/PanPredic/tests/data/panResults2/accessoryGenomeFragments.fasta')
    sequence_count = 0
    match_count = 0
    #with open ('/home/james/backend/app/modules/PanPredic/tests/data/sequence_errors.fasta', 'a+') as f:
    for header in seq_dict:
        sequence_count = sequence_count + 1
        seq = seq_dict[header]
        if header in seq_dict2:
            match_count = match_count + 1
            print('SUCCESS')
        else:
            print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
            print('FAILURE')
            header = '>' + header + '\n'
            print(header)
            print(seq)
            #seq = seq + '\n'
            #f.write(header)
            #f.write(seq)
            print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')



    print(sequence_count)
    print(match_count)
