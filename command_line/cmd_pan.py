import os
from modules.PanPredic.SVM import svm_bovine
from modules.PanPredic.cmd_uploader import cmd_workflow, pred_workflow
from modules.PanPredic.pan_run import panseq
from modules.PanPredic.conf_gen import generate_conf, gen_match_pred
from modules.PanPredic.definitions import PAN_RESULTS
from modules.PanPredic.pan_utils import sym_linker, tagger, dir_merge
import cPickle as pickle
from datetime import datetime
from modules.PanPredic.definitions import ROOT_DIR
from pan_run import cmd_prediction
import shutil

pickle_file = ROOT_DIR + '/hbpickles.p'
clf_pickle = ROOT_DIR +'/clfpickle.p'
pred_pickle = ROOT_DIR+ '/predpickle.p'


def pan(args_dict):

    print('root : '+ ROOT_DIR)

    query_pos = args_dict['p']

    query_neg = args_dict['n']

    now = datetime.now()
    now = now.strftime("%Y-%m-%d-%H-%M-%S-%f")

    query_files = query_pos + '/copies_' + now
    print(query_files)
    os.mkdir(query_files)
    tagger(query_pos, '_pos', query_files)
    tagger(query_neg, '_neg', query_files)





    prediction_files = args_dict['q']


    #create a unique filename




    # (1) generate conf files, these specify locations of genomes as well as panseq run parameters
    #stores them in a dictionary {novel: conf_file, match: conf_file}
    query_dict = generate_conf(query_files)



    # (2) run panseq
    panseq(query_dict)
    shutil.rmtree(query_files)


    results = parse()
    prediction(results, prediction_files)

def parse():
    # (3) Parse panseq results
    results_dict = cmd_workflow(PAN_RESULTS + '/pan_genome.txt')

    pickle_file = ROOT_DIR + '/hbpickles.p'
    pickle.dump(results_dict, open(pickle_file, 'wb'))

    return results_dict

def prediction(results_dict, prediction_files):

    # (5) prediction

    clf, sel = svm_bovine(results_dict)
    #pickle.dump(clf, open(clf_pickle, 'wb'))

    pred_conf = gen_match_pred(prediction_files)

    #run panseq against training set with predicting set
    cmd_prediction(pred_conf)
    #parse predicting pangenome

    prediction_dict = pred_workflow(PAN_RESULTS + '_pred/pan_genome.txt')
    pickle.dump(prediction_dict, open(pred_pickle, 'wb'))

    X =[]
    successes = 0
    failures = 0
    for genome in prediction_dict:
        print(genome)
        X = [(prediction_dict[genome]['values'])]
        print('before transform:')
        print(len(X[0]))
        X = sel.fit_transform(X)
        print(len(X[0]))
        pred = clf.predict(X)

        print(pred)
        #must do the same feature selection on training data and on prediction data
        if genome.startswith('ine') and pred == 1:
            successes = successes + 1
        if genome.startswith('an') and pred == 0:
            successes = successes + 1
        if genome.startswith('ine') and pred == 0:
            failures = failures + 1
        if genome.startswith('an') and pred == 1:
            failures = failures + 1
    #X = sel.fit_transform(X)
    print(clf.predict(X))
    print successes
    print failures




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
        "-p",
        help="directory of FASTA files, positive for trait",
        required=True
        )
    parser.add_argument(
        "-n",
        help="directory of FASTA files, negative for trait",
        required=True
        )
    parser.add_argument(
        "-q",
        help="directory of FASTA files, to make predictions for",
        required=True
        )

    args = parser.parse_args()
    args_dict = vars(args)



    print(args_dict)
    args_dict['p'] = os.path.abspath(args_dict['p'])
    args_dict['n'] = os.path.abspath(args_dict['n'])
    args_dict['q'] = os.path.abspath(args_dict['q'])

    print(pan(args_dict))


'''
