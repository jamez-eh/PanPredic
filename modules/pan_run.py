import subprocess
import sys
import shutil
from app.modules.PanPredic.definitions import ROOT_DIR
from app.modules.PanPredic.modules.queries import query_panseq
import os
from app.modules.PanPredic.modules.pandas_parsing import sequence_counter

args = 'perl lib/panseq.pl settings.txt'

def panseq(query_dict):


    match_config = str(query_dict['match'])
    novel_config = str(query_dict['novel'])

    #TODO: make this query safe for very large lists (with more genomes this will break)
    pan_list = query_panseq()


    if pan_list:
        #build the fasta file required as a queryfile for the pan run
        query_file = build_pan(pan_list)
        print('QUERYFILE COUNT PRE JOIN: \n')
        print(sequence_counter(query_file))


        #run panseq to find novel pangenome regions
        novel = subprocess.Popen(["perl", "/home/james/Panseq/lib/panseq.pl", novel_config], stdout=sys.stdout)
        novel.communicate()
        
        print('NOVEL REGIONS COUNT: \n')
        print(sequence_counter('/home/james/backend/app/modules/PanPredic/tests/data/novelResults/novelRegions.fasta'))


        # append these pangenome regions to current pangenome fastareference
        join_files(query_file, ROOT_DIR + '/tests/data/novelResults/novelRegions.fasta')
        print('QUERYFILE COUNT POST JOIN: \n')
        print(sequence_counter(query_file))

    #finds a full set of pangenome regions for the queried genomes
    match = subprocess.Popen(["perl", "/home/james/Panseq/lib/panseq.pl", match_config], stdout=sys.stdout)

    match.communicate()

    print('TOTAL PAN REGIONS COUNT: \n')
    print(sequence_counter('/home/james/backend/app/modules/PanPredic/tests/data/panResults/accessoryGenomeFragments.fasta'))

    if pan_list:
        os.remove(query_file)


#TODO: protect this from large files (don't read all of it into memory) ->do with pandas

#TODO: whenever there is a file being appended, check to see if it exists first, and delete if so
#joins two files together
def join_files(file1, file2):
    """
    :param :
       two text files
    :return: 
        a single text file with the second appended to the first
    """

    #read file to append it to next file
    second = open(file2, "r")
    data = second.read()
    second.close()

    #append second file to the first
    first = open(file1, "a")
    first.write(data)
    first.close()


#builds a pangenome by querying blazegraph
def build_pan(pan_list):
    """
    :param :
       pangenome as a list 
    :return: 
        the complete pangenome as a fasta file 
        
    """

    filename = ROOT_DIR + '/Data/PanGenomeRegions.fasta'
    i = 1
    for entry in pan_list:
        if i % 2 != 0:
            f = open(filename, "a+")
            f.write('>' + entry + '\n')
        else:
            f = open(filename, "a+")
            f.write(entry + '\n')
        f.close()
        i = i + 1
    return filename








