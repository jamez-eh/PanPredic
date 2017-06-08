from app.modules.PanPredic.modules.pan_run import panseq
from app.modules.PanPredic.modules.uploader import workflow
from app.modules.PanPredic.modules.conf_gen import generate_conf
from app.modules.PanPredic.definitions import PAN_RESULTS, NOVEL_RESULTS
from app.modules.PanPredic.modules.grapher import generate_graph


def pan(args_dict):

    query_files = args_dict['i']

    # (1) generate conf files
    query_dict = generate_conf(query_files)

    # (2) run panseq
    panseq(query_dict)

    # (3) Parse panseq results
    results_pickle = workflow(PAN_RESULTS + '/pan_genome.txt', PAN_RESULTS + '/accessoryGenomeFragments.fasta', query_files)

    return results_pickle

    # (4) create graph
    generate_graph()
    # (5) analyze pan data

dict = {}
dict['i'] = '/home/james/backend/app/modules/PanPredic/tests/data/filteredgenomes'

pan(dict)
