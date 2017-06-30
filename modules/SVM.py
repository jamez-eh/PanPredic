from sklearn import svm
from sklearn.naive_bayes import BernoulliNB

from app.modules.PanPredic.modules.queries import get_genomes
from app.modules.PanPredic.modules.data_shape import get_data, get_vectors
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


