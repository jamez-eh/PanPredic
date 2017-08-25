
from modules.PanPredic.uploader import workflow
from modules.PanPredic.pan_run import panseq, sym_linker
from modules.PanPredic.conf_gen import generate_conf
from modules.PanPredic.definitions import PAN_RESULTS
import pickle
from modules.loggingFunctions import initialize_logging
import logging
from datetime import datetime
from modules.PanPredic.grapher import create_graph


def pan(args_dict, pickle_file):
    

    query_files = args_dict['i']
    #create a unique filename
    now = datetime.now()
    now = now.strftime("%Y-%m-%d-%H-%M-%S-%f")
    

    #create a subdirectory with symlinks to original files (keeps directory clean)
    query_files = sym_linker(query_files)
   
    # (1) generate conf files, these specify locations of genomes as well as panseq run parameters
    #stores them in a dictionary {novel: conf_file, match: conf_file}
    query_dict = generate_conf(query_files)

    
    # (2) run panseq
    panseq(query_dict)


    # (3) Parse panseq results

    results_dict= workflow(PAN_RESULTS + '/pan_genome.txt', PAN_RESULTS + '/accessoryGenomeFragments.fasta', query_files)


    pickle.dump(results_dict, open(pickle_file, 'wb'))



    # (5) prediction
    #prediction()

    return 'SUCCESS'





