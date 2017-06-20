from sklearn import datasets
from sklearn import svm
from app.modules.PanPredic.modules.queries import gen_pan, pan_names
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
def get_data():

    #get a list of genomes and associated pan genome regions
    gen_pan_list = gen_pan()
    pan_genome = pan_names()


#get_data()

