import subprocess
import sys
import shutil
from app.modules.PanPredic.definitions import ROOT_DIR


args = 'perl lib/panseq.pl settings.txt'

def panseq(query_dict):

    match_config = str(query_dict['match'])
    novel_config = str(query_dict['novel'])

    #run panseq to find novel pangenome regions
    novel = subprocess.Popen(["perl", "/home/james/Panseq/lib/panseq.pl", novel_config], stdout=sys.stdout)
    novel.communicate()

    # append these pangenome regions to current pangenome fastareference
    join_files(ROOT_DIR + '/PanGenomeRef/coreGenomeFragments.fasta', match_config)

    #finds a full set of pangenome regions for the queried genomes
    match = subprocess.Popen(["perl", "/home/james/Panseq/lib/panseq.pl", match_config], stdout=sys.stdout)
    match.communicate()



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
    i = 1
    for entry in pan_list:
        if i % 2 != 0:
            f = open(ROOT_DIR + '/Data/PanGenomeRegions.fasta', "a")
            f.write('>' + entry + '\n')
        else:
            f = open(ROOT_DIR + '/Data/PanGenomeRegions.fasta', "a")
            f.write(entry + '\n')
        f.close()
        i = i + 1
    return f








