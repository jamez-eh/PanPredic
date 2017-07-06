from app.modules.PanPredic.modules.pan_run import panseq, sym_linker
from app.modules.PanPredic.modules.uploader import workflow
from app.modules.PanPredic.modules.conf_gen import generate_conf
from app.modules.PanPredic.definitions import PAN_RESULTS, NOVEL_RESULTS
from app.modules.PanPredic.modules.grapher import create_graph
from app.modules.PanPredic.definitions import ROOT_DIR
import pickle
from app.modules.loggingFunctions import initialize_logging
import logging
import pdb


log_file = initialize_logging()
log = logging.getLogger(__name__)


def pan(args_dict):

    query_files = args_dict['i']

    pickle_file = query_files + '/p_pasneq.p'

    #create a subdirectory with symlinks to original files (keeps directory clean)
    query_files = sym_linker(query_files)

    # (1) generate conf files
    query_dict = generate_conf(query_files)
    log.debug('query dict:' + str(query_dict))

    # (2) run panseq
    panseq(query_dict)
    log.debug('panseq finished')

    # (3) Parse panseq results
    print('Parsing')
    results_dict= workflow(PAN_RESULTS + '/pan_genome.txt', PAN_RESULTS + '/accessoryGenomeFragments.fasta', query_files)
    log.debug('panseq parsed:'+ str(results_dict))

    pickle.dump(results_dict, open(pickle_file, 'wb'))

    # (4) create graph
    create_graph(results_dict)
    #log.debug('graph finished: ' + str(pan_turtle))

    # (5) prediction
    #prediction()



dict = {}
dict['i'] = '/home/james/backend/app/modules/PanPredic/tests/data/filteredgenomes'

pan(dict)








