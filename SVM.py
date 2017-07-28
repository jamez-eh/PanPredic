from sklearn import svm
from sklearn.feature_selection import VarianceThreshold
from sklearn.naive_bayes import BernoulliNB

from modules.PanPredic.queries import get_genomes
from modules.PanPredic.data_shape import get_data, get_vectors, bovinator
import pickle



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

    #select features with a high amount of variance

    clf = svm.SVC()

    sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
    sel.fit_transform(X)

    clf.fit(X,y)

    return clf, sel
