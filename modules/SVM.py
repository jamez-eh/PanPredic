from sklearn import datasets
from sklearn import svm
from app.modules.PanPredic.modules.queries import gen_pan, pan_names, get_virulence, vir_names, get_genomes
import pickle
'''
digits = datasets.load_digits()
print('all')
print(digits)
print('features:')
print(digits.data)

print('labels: ')
print(digits.target)



#predict using model called clf

'''
#TODO: move the data getting functions into a different module
#ideas to make this better -> use pandas dataframes, first get list of genomes and then for each genome query ->store in file and merge results, use memmaps or mmaps (memmaps lets us store in lists, which is what svm takes)
#TODO: Refactor so that we use sets instead of lists, speed vs memory???

def get_data():

    #get a list of genomes and associated pan genome regions
    gen_panreg = gen_pan()
    pan_genome = pan_names()

    return eval_vectors(gen_panreg, pan_genome)


#make a vector of 1's and 0's for each genome so that we can see presence or absence of pangenome regions
def eval_vectors(gen_pan, pan_genome):
    '''
    
    :param gen_pan: a dictorary in form {genome: [region, ....], genome:  .........}
    :param pan_genome: a list of all pangenome regions
    :return: vector_dict: a dictionary of genomes with assoc bitmap vector of presence or abscence of a pangenome region 
    '''

    vector_dict = {}

    for genome in gen_pan:

        vector_dict[genome] = []

        for pan in pan_genome:

            if pan in gen_pan[genome]:
                vector_dict[genome].append(1)
            else:
                vector_dict[genome].append(0)

    return vector_dict


#TODO: refactor so that it is more general use (accept an argument to dictate which kind of label -> location, virulence, amr etc)



def get_vectors(region):
    '''
    
    :return: X and y vectors for svm training
    '''

    X = []
    y = []


    pans = get_data()
    virs = get_genomes(region)

    #assigning vectors like this keeps pan genome regions and AMR, vir, etc in sync
    for genome in pans:
        X.append(pans[genome])
        if genome in virs:
            y.append(1)
        else:
            y.append(-1)

    return X, y


def training(X, y):


    clf = svm.SVC()

    clf.fit(X,y)

    yo = clf.predict(X[1])

    print(yo)






def prediction(region):
    '''
    
    :param region: the amr or virulence factor etc that we are interested in
    :return: 
    '''

    X, y = get_vectors(region)

    training(X, y)


