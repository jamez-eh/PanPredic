import modules.pan_run
import modules.uploader

def pan():

    # (1) generate conf files

    # (2) run panseq
     modules.pan_run.pan_run()

    # (3) Parse panseq results
    results_dict = modules.uploader.workflow()

    # (4) upload pan data to blazegraph

    # (5) analyize pan data

