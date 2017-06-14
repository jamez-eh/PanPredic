from app.modules.PanPredic.modules.pan_run import panseq
from app.modules.PanPredic.modules.uploader import workflow
from app.modules.PanPredic.modules.conf_gen import generate_conf
from app.modules.PanPredic.definitions import PAN_RESULTS, NOVEL_RESULTS
from app.modules.PanPredic.modules.grapher import create_graph
from app.modules.PanPredic.definitions import ROOT_DIR
import pickle
from app.modules.loggingFunctions import initialize_logging
import logging

log_file = initialize_logging()
log = logging.getLogger(__name__)


def pan(args_dict):

    pickle_file = ROOT_DIR + '/results_pickle.p'

    query_files = args_dict['i']

    # (1) generate conf files
    query_dict = generate_conf(query_files)
    log.debug('query dict:' + str(query_dict))

    # (2) run panseq
    panseq(query_dict)
    log.debug('panseq finished')

    # (3) Parse panseq results
    results_dict= workflow(PAN_RESULTS + '/pan_genome.txt', PAN_RESULTS + '/accessoryGenomeFragments.fasta', query_files)
    log.debug('panseq parsed:'+ str(results_dict))

    #pickle.dump(results_dict, open(pickle_file, 'wb'))

    # (4) create graph
    pan_turtle = create_graph(results_dict)
    log.debug('graph finished: ' + str(pan_turtle))

    return pan_turtle



dict = {}
dict['i'] = '/home/james/backend/app/modules/PanPredic/tests/data/filteredgenomes'

pan(dict)

'''
results_dict = pickle.load(open(ROOT_DIR + '/results_pickle.p', 'rb'))

graph = create_graph(results_dict)
'''