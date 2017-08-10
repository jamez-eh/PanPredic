import pandas as pd
import numpy as np
import shutil
from modules.PanPredic.pan_utils import tagger
import os
from modules.PanPredic.pan_run import panseq
import re
import pdb
from modules.PanPredic.conf_gen import generate_conf
from modules.PanPredic.cmd_pan import parse
from SVM import alternator
'''
df = pd.read_csv('/home/james/ecoli_omnilog/data/omnilog_data_summary.txt', sep=None)

df2 = pd.read_csv('/home/james/ecoli_omnilog/omnilog_well_descriptions2.txt', sep='\t')

pheno_list = []


pheno_list = df2['phenotype'].tolist()
index = 0
for well in pheno_list:
    m = re.search('(?<=\()(.*?)(?=\))', well)
    pheno_list[index] = m.group(0)
    index = index + 1

    
df = df[df['label'].isin(pheno_list)]

mask = df.value <= 50
column_name = 'value'
df.loc[mask, column_name] = 1

mask = df.value > 50
column_name = 'value'
df.loc[mask, column_name] = 0

df.to_csv('data_labels.txt', sep='\t', encoding='utf-8')



print(df)


                    
'''


def cv_reader():
                
    df = pd.read_csv('/home/james/data_labels.txt', sep='\t')
    df = df.sort_values(['label'], ascending=[False])

    return df



def label_maker(df):
    '''
    param: df with columns: index, name, label, value sorted by label
    returns: label_dict: {label: {name: value, name: value.. }, ...}
    '''
    
    label_dict = {}
    label_index = 'initial'
    #pdb.set_trace()
    for row in df.iterrows():
        index, data = row
        row_list = data.tolist()
        if label_index != row_list[2]:
            label_index = row_list[2]
            df2 = df[df['label'] == label_index]
            df2 = df2.sort_values(['name'], ascending=[False])

            #group duplicates and average their values
            df2 = df2.groupby('name', as_index=False).mean()

    
            label_dict[label_index] = {}
           
            for sub_row in df2.iterrows():
                index, data = sub_row
                row_list = data.tolist()
                genome = row_list[0]
                presence = row_list[2]
                label_dict[label_index][genome] = presence
           
    return label_dict



def get_genome_vectors(dir):
    '''
    os.mkdir('/home/james/renamed_files')
    renamed_files = tagger(dir, '', '/home/james/renamed_files')
    query_dict = generate_conf('/home/james/renamed_files')
    panseq(query_dict)
    '''
    results_dict = parse()
    #shutil.rmtree('/home/james/renamed_files')
    return results_dict


def multi_test():

    df = cv_reader()
    labels = label_maker(df)
    genome_vectors = get_genome_vectors('/home/james/sequences')
    #pdb.set_trace()
    label_vectors = {}
    for label in labels:
        y = []
        X = []
        vector_dict = {}
       
        for genome in labels[label]:
            #pdb.set_trace()
            
            if genome in genome_vectors:
                if labels[label][genome] > 50:
                    y.append(1)
                else:
                    y.append(0)
                X.append(genome_vectors[genome]['values'])
            else:
                print('genome not found: ' )
                print(genome)

        vector_dict = {'X': np.array(X), 'y': np.array(y)}
        label_vectors[label] = vector_dict
    
    svm, sel = alternator(label_vectors)


multi_test()
