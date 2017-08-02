from sklearn import svm
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.feature_selection import VarianceThreshold
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import cross_val_score
from modules.PanPredic.queries import get_genomes
from modules.PanPredic.data_shape import get_data, get_vectors, bovinator
import pickle
from matplotlib import pyplot as plt
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn.datasets import make_classification
from sklearn.svm import SVC
import numpy as np


'''
Wrappers for scikit-learn.org modules 
'''

#TODO: make these functional




def svm_predict(region, genome_vector):
    '''
    
    :param region: the amr or virulence factor etc that we are interested in
           genome_vector: a pan genome bit map for genome of interest
    :return: 0 if prediction is false, 1 if prediction is true
    '''

    X, y = get_vectors(region)

    clf = svm.SVC()

    clf.fit(X,y)

    return clf.predict(genome_vector)





def bayes_predict(region, genome_vector):
    '''

    :param region: the amr or virulence factor etc that we are interested in
           genome_vector: a pan genome bit map for genome of interest
    :return: 0 if prediction is false, 1 if prediction is true
    '''

    X, y = get_vectors(region)

    clf = BernoulliNB()

    clf.fit(X, y)

    return clf.predict(genome_vector)



def svm_bovine(pan_dict):

    '''
    for bovine/human set only, returns a clf after fitting with data.
    '''
    X,y = bovinator(pan_dict)
    
    # an additional svm is made here, used only to analyze feature selection
    svc = SVC(kernel="linear", C=0.01)
    svc_rbf = SVC(kernel="rbf")
    svc_poly = SVC(kernel="poly")

    cross_val_variance(svc, X, y, 10)

   

   
    #recursive feature selection and graph
    '''
    rfecv = RFECV(estimator=svc, step=1, cv=StratifiedKFold(2),
                                scoring='accuracy')

    

    
    rfecv.fit(X, y)
    opt_feature_num(rfecv)
    '''
    param_opt(X, y)


    clf.fit(X,y)

    
    return clf, sel

def param_opt(X, y):

    param_range = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]

    param_grid = [{'C': param_range,
                   'kernel': ['linear']},
                  {'C': param_range,
                   'gamma': param_range,
                   'kernel' : ['rbf']}]
    
    gs = GridSearchCV(estimator=SVC(C=1),
                      param_grid = param_grid,
                      scoring='accuracy',
                      cv=10,
                      n_jobs=-1)
    gs = gs.fit(X, y)
    print(gs.best_score_)
    print(gs.best_params_)

def cross_val_variance(model, X, y, cv):
    print(X.shape[1])

    var = 0.0
    best = 0.0
    while (var < 0.5):
        print(var)
        #select features with a high amount of variance
        sel = VarianceThreshold(threshold=(var * (1 - var)))
        X_sel = sel.fit_transform(X)
        print(X_sel.shape[1])
    

    
        clf = svm.SVC(kernel='linear')
        #cross validation of clf with the parameters above (including feature selection
        scores = cross_val_score(
            model, X_sel, y, cv=10)

        print(scores)
        average = sum(scores)/len(scores)
        print('Average: ' + str(average))
        if average > best:
            best = average
        print('Best: ' + str(best))
        var = var + 0.01
    



#takes the coefficents from coef_ in linear SVM and then 

def inf_features(coef, names):
    '''
    param: coef: coef_ from a linear svm, the scores of each attr after fitting
    param: names: the actual names associated to each coef
    creates a bar graph of the 20 highest scoring names
    '''
    imp = coef
    imp,names = zip(*sorted(zip(imp,names)))
    plt.barh(StratifiedKFold,
             RFECV, imp, align='center')
    plt.yticks(20, names)
    plt.show()
                    

def opt_feature_num(rfecv):
    plt.xlabel("Number of features selected")
    plt.ylabel("Cross validation score (nb of correct classifications)")
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
    plt.show()
