from modules.PanPredic.definitions import ROOT_DIR, PAN_RESULTS, NOVEL_RESULTS
#from modules.PanPredic.queries import check_panseq
import os
from platform import system
import subprocess
import re




def program_loc():

    cmd = "where" if system() == "Windows" else "which"
    try:
        
        muscle = subprocess.check_output([cmd, 'muscle'])
        mummer = subprocess.check_output([cmd, 'mummer'])
        blast = subprocess.check_output([cmd, 'blastn'])

        muscle = re.search('(.*?)(?=muscle)', muscle)
        mummer = re.search('(.*?)(?=mummer)', mummer)
        blast = re.search('(.*?)(?=blastn)', blast)
        
       
        muscle = muscle.group(0)
        mummer = mummer.group(0)
        blast = blast.group(0)
        '''
        #this is a cheat, and is not ideal
        muscle = '/opt/conda/envs/backend/bin/'
        mummer = '/opt/conda/envs/backend/bin/'
        blast = '/opt/conda/envs/backend/bin/'
        '''
        return muscle, mummer, blast



    except Exception as error:
        print('Blast, mummer, and muscle are not all installed correctly. Please check installations of these programs')
        return 'nothing', 'nothing', 'nothing'


def gen_novel(genome_files):

    muscle, mummer, blast = program_loc()

    with open(ROOT_DIR + '/panseq_novel_pangenome.conf', 'wb') as f:
        f.writelines([b'queryDirectory   ' + genome_files.encode() + b'\n',
                    b'referenceDirectory '	+ ROOT_DIR.encode() + b'/Data \n',
                    b'baseDirectory  ' + NOVEL_RESULTS.encode() + b'\n',
                    b'numberOfCores	4 \n',
                    b'mummerDirectory '	+ mummer.encode() + '\n',
                    b'blastDirectory ' + blast.encode() +  '\n',
                    b'minimumNovelRegionSize	500 \n',
                    b'novelRegionFinderMode	no_duplicates \n',
                    b'muscleExecutable ' + muscle + '\n',
                    b'percentIdentityCutoff	95 \n',
                    b'runMode	novel \n',
                    b'overwrite 1 \n',
                      b'sha1 1 \n'])
        return ROOT_DIR + '/panseq_novel_pangenome.conf'


def gen_match(genome_files):

    muscle, mummer, blast = program_loc()

    settings_list = [b'queryDirectory   ' + genome_files.encode() + b'\n',
                    b'baseDirectory  '  +  PAN_RESULTS.encode() + b'\n',
                    b'numberOfCores	5 \n',
                    b'mummerDirectory '	+ mummer.encode() + '\n',
                    b'blastDirectory ' + blast.encode() +  '\n',
                    b'muscleExecutable ' + muscle + '\n',
                     b'fragmentationSize	500 \n',
                     b'minimumNovelRegionSize    500 \n',
                    b'percentIdentityCutoff	95 \n',
                     b'maxNumberResultsInMemory    125 \n',
                    b'coreGenomeThreshold   1000000000 \n',
                    b'runMode	pan \n',
                    b'nameOrId	id \n',
                    b'overwrite 1 \n',
                     b'sha1 1 \n']

   # pan_list = check_panseq()


    #if pan_list and not cmd:
    #    settings_list.insert(1, b'queryFile  ' +  ROOT_DIR.encode() +  b'/Data/PanGenomeRegions.fasta\n')



    with open(ROOT_DIR + '/panseq_pan_pangenome.conf', 'wb') as f:
        f.writelines(settings_list)
        return ROOT_DIR + '/panseq_pan_pangenome.conf'

def gen_match_pred(genome_files):
    muscle, mummer, blast = program_loc()

    settings_list = [b'queryDirectory   ' + genome_files.encode() + b'\n',
                    b'baseDirectory  '  +  PAN_RESULTS.encode() + b'_pred\n',
                     b'queryFile    ' + PAN_RESULTS.encode() + b'/Data/accessoryGenomeFragments.fasta',
                    b'numberOfCores	5  \n',
                    b'mummerDirectory '	+ mummer.encode() + '\n',
                    b'blastDirectory ' + blast.encode() +  '\n',
                    b'muscleExecutable ' + muscle + '\n',
                     b'maxNumberResultsInMemory    125 \n',
                    b'percentIdentityCutoff	95 \n',
                    b'coreGenomeThreshold   1000000000 \n',
                    b'minimumNovelRegionSize    500 \n',
                    b'runMode	pan \n',
                    b'nameOrId	id \n',
                    b'overwrite 1 \n',
                     b'sha1 1 \n']

   # pan_list = check_panseq()


    #if pan_list and not cmd:
    #    settings_list.insert(1, b'queryFile  ' +  ROOT_DIR.encode() +  b'/Data/PanGenomeRegions.fasta\n')



    with open(ROOT_DIR + '/panseq_pred_pangenome.conf', 'wb') as f:
        f.writelines(settings_list)
        return ROOT_DIR + '/panseq_pred_pangenome.conf'

#driver function generates both necessary conf files
def generate_conf(genome_files):

    query_dict = {}

    query_dict['novel'] = gen_novel(genome_files)
    query_dict['match'] = gen_match(genome_files)
    
    return query_dict

