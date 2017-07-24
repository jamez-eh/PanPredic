import subprocess
import sys
import shutil
from modules.PanPredic.definitions import ROOT_DIR
from modules.PanPredic.queries import query_panseq
import os
from modules.PanPredic.pandas_parsing import sequence_counter
from platform import system
from datetime import datetime

#TODO: add src to definitions and dst to definitions
def sym_linker(file_list):
    '''
    Creates a subdirectory in the query directory with symlinks to all the fasta files, 
    necessary for panseq to run with all the junk that other process place in the query dir
    :param a list of files
    :param dst: destination directory
    :return: source directory
    '''
    now = datetime.now()
    now = now.strftime("%Y-%m-%d-%H-%M-%S-%f")
    dst = '/datastore/' +  str(now) + '_panseq_syms'
    try:
        os.mkdir(dst)
    except:
        print(dst + ' already exists')


    for file in file_list:
        if file.endswith('.fna') or file.endswith('.fasta'):
            try:
                os.symlink(file, dst + '/' + os.path.basename(file))
            except:
                print(dst + '/' + file +' already exists')


    return dst





def pan_loc():

    cmd = "where" if system() == "Windows " else "which"
   
    try:
        panseq = subprocess.check_output([cmd, 'panseq'])
        
        return panseq
              
    except Exception as error:
        print('panseq installation not found')




def panseq(query_dict):
    '''
    Runs panseq, if there are already pangenome regions in blazegraph, it pulls these down to form a current pangenome, 
    novel is then run against these and appended to the original pangenome before running panseq in panmode
    :param query_dict: 
    :return: 
    '''
    #panseq = pan_loc()

    match_config = str(query_dict['match'])
    novel_config = str(query_dict['novel'])

    #TODO: make this query safe for very large lists (with more genomes this will break)
    pan_list = query_panseq()


    if pan_list:
        #build the fasta file required as a queryfile for the pan run
        query_file = build_pan(pan_list)
        #print('QUERYFILE COUNT PRE JOIN: \n')
        #print(sequence_counter(query_file))


        #run panseq to find novel pangenome regions
        novel = subprocess.Popen(["panseq", novel_config], stdout=sys.stdout)
        novel.communicate()

        #print('NOVEL REGIONS COUNT: \n')
        #print(sequence_counter('/home/james/backend/app/modules/PanPredic/tests/data/novelResults/novelRegions.fasta'))


        # append these pangenome regions to current pangenome fastareference
        join_files(query_file, ROOT_DIR + '/tests/data/novelResults/novelRegions.fasta')
        #print('QUERYFILE COUNT POST JOIN: \n')
        #print(sequence_counter(query_file))

    #finds a full set of pangenome regions for the queried genomes
            
    match = subprocess.Popen(['panseq', match_config], stdout=sys.stdout)


    match.communicate()


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








