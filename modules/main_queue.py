import modules.pan_run
import modules.uploader
import modules.conf_gen
from definitions import PAN_RESULTS, NOVEL_RESULTS

def pan(args_dict):

    # (1) generate conf files
    query_dict = modules.conf_gen.generate_conf(args_dict['genomes'])

    # (2) run panseq
    modules.pan_run.panseq(query_dict)

    # (3) Parse panseq results
    results_pickle = modules.uploader.workflow(PAN_RESULTS + '/pan_genome.txt', PAN_RESULTS + '/coreGenomeFragments.fasta')

    # (4) upload pan data to blazegraph

    # (5) analyze pan data

dict = {}
dict['genomes'] = '/home/james/backend/app/modules/PanPredic/tests/data/filteredgenomes'

pan(dict)