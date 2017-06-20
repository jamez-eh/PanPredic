from sklearn import datasets
from sklearn import svm
from app.modules.PanPredic.modules.queries import gen_pan, pan_names, get_virulence
'''
digits = datasets.load_digits()
print('all')
print(digits)
print('features:')
print(digits.data)

print('labels: ')
print(digits.target)

clf = svm.SVC()

clf = svm.SVC(gamma=0.001, C=100)

X,y = digits.data[:-10], digits.target[:-10]

#train
clf.fit(X,y)

#predict using model called clf
print(clf.predict(digits.data[-5]))
'''

#ideas to make this better -> use pandas dataframes, first get list of genomes and then for each genome query ->store in file and merge results, use memmaps or mmaps (memmaps lets us store in lists, which is what svm takes)
#TODO: Refactor so that we use sets instead of lists, speed vs memory???

def get_data():

    #get a list of genomes and associated pan genome regions
    gen_panreg = gen_pan()
    pan_genome = pan_names()

    return gen_panreg, pan_genome


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
def get_labels():
    '''
    
    :return: a list of all labels for 
    '''

    vir = get_virulence()

    return vir

