import subprocess
import sys
import shutil
from definitions import ROOT_DIR


args = 'perl lib/panseq.pl settings.txt'

def panseq():

    #run panseq to find novel pangenome regions
    novel = subprocess.Popen(["perl", "/home/james/Panseq/lib/panseq.pl", "/home/james/pan_genome/PanPredic/panseq_findnew_pangenome.conf"], stdout=sys.stdout)
    novel.communicate()

    # append these pangenome regions to current pangenome fastareference
    join_files(ROOT_DIR + '/PanGenomeRef/coreGenomeFragments.fasta', ROOT_DIR + '/novelPanResults/novelRegions.fasta')

    #TODO: Pass to database uploader

    #deletes the novel results AFTER they are appended to the pangenome and the
    #shutil.rmtree('/home/james/pan_genome/PanPredic/PanResults')

    #finds a full set of pangenome regions for the queried genomes
    match = subprocess.Popen(["perl", "/home/james/Panseq/lib/panseq.pl", "/home/james/pan_genome/PanPredic/panseq_match_pangenome.conf"], stdout=sys.stdout)
    match.communicate()

    shutil.rmtree('/home/james/pan_genome/PanPredic/PanResults2')


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




panseq()