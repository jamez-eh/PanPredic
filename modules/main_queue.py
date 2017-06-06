import modules.pan_run
import modules.uploader
import modules.conf_gen

def pan(args_dict):


    # (1) generate conf files
    query_dict = modules.conf_gen.generate_conf(args_dict['genomes'])

    # (2) run panseq
    modules.pan_run.panseq(query_dict)

    # (3) Parse panseq results
    results_pickle = modules.uploader.workflow()

    # (4) upload pan data to blazegraph

    # (5) analyze pan data


pan