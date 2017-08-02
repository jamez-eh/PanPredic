from sklearn import svm
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
    svc = SVC(kernel="linear")
    #recursive feature selection and graph
    rfecv = RFECV(estimator=svc, step=1, cv=StratifiedKFold(2),
                                scoring='accuracy')

    

    
    #rfecv.fit(X, y)
    #opt_feature_num(rfecv)




    #select features with a high amount of variance
    sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
    #sel.fit_transform(X)
    #sel.fit_transform(y)

    print(np.unique(map(len, X)))
    clf = svm.SVC(kernel='linear')
    #cross validation of clf with the parameters above (including feature selection
    #scores = cross_val_score(
    #    clf, X, y, cv=5)
    
    clf.fit(X,y)

    
    return clf, sel



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
