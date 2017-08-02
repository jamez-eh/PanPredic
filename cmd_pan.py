import os
from modules.PanPredic.SVM import svm_bovine
from modules.PanPredic.cmd_uploader import cmd_workflow
from modules.PanPredic.pan_run import panseq, sym_linker
from modules.PanPredic.conf_gen import generate_conf, gen_match_pred
from modules.PanPredic.definitions import PAN_RESULTS
import cPickle as pickle
from datetime import datetime
from modules.PanPredic.definitions import ROOT_DIR
from pan_run import cmd_prediction


pickle_file = ROOT_DIR + '/hbpickles.p'
clf_pickle = ROOT_DIR +'/clfpickle.p'
pred_pickle = ROOT_DIR+ '/predpickle.p'

def pan(args_dict):
    

    query_files = args_dict['i']
    prediction_files = args_dict['q']
    pickle_file = ROOT_DIR + '/hbpickles.p'

    pred_pickle = ROOT_DIR+ '/predpickle.p'
    #create a unique filename
    now = datetime.now()
    now = now.strftime("%Y-%m-%d-%H-%M-%S-%f")

    # (1) generate conf files, these specify locations of genomes as well as panseq run parameters
    #stores them in a dictionary {novel: conf_file, match: conf_file}
    query_dict = generate_conf(query_files)
    
    

    # (2) run panseq
    panseq(query_dict)

    results = parse()
    prediction(results)
    
def parse():
    # (3) Parse panseq results
    results_dict = cmd_workflow(PAN_RESULTS + '/pan_genome.txt')
    

    pickle.dump(results_dict, open(pickle_file, 'wb'))

    return results_dict    

def prediction(results_dict, prediction_files):
    
    # (5) prediction

    clf, sel = svm_bovine(results_dict)
    pickle.dump(clf, open(clf_pickle, 'wb'))

    pred_conf = gen_match_pred(prediction_files)

    #run panseq against training set with predicting set
    cmd_prediction(pred_conf)
    #parse predicting pangenome
    prediction_dict = cmd_workflow(PAN_RESULTS + '_pred/pan_genome.txt')
    pickle.dump(prediction_dict, open(pred_pickle, 'wb'))

    for genome in prediction_dict:
        print(genome)
        X = prediction_dict[genome]['values']
        #must do the same feature selection on training data and on prediction data
        #sel.fit_transform(X)
        print(clf.predict(X))


    
    #test_files = os.listdir(prediction_files):
    #test_syms = sym_linker(test_files)


#parse()

the_pickle = open(ROOT_DIR + '/hbpickles.p', 'rb')
print("loading pickle")
#the_pickle.seek(0)
results_dict = pickle.load(the_pickle)
the_pickle.close()

print("pickle loaded")
prediction(results_dict, '/home/james/HB')
'''
    


if __name__ == "__main__":
    import argparse              

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        help="directory of FASTA files",
        required=True
        )
    parser.add_argument(
        "-q",
        help="directory of files to make predictions for",
        required=True
        )
    
    args = parser.parse_args()
    args_dict = vars(args)

    
    
    print(args_dict)
    args_dict['i'] = os.path.abspath(args_dict['i'])

    print(pan(args_dict))



'''
