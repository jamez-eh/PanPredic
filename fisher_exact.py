import logging
from modules.loggingFunctions import initialize_logging
import scipy.stats as stats
import pandas as pd
from modules.PanPredic.data_shape import get_labels, get_data
from statsmodels.stats.multitest import multipletests

#TODO: make all arrays numpy arrays

# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)




def fishers():


    data = get_data()
    labels = get_labels()

    p_matrix = []
    pos = [0, 0]
    neg = [0, 0]
    #never need to reset amr index because once we get through each amr we are done
    amr_index = 0

    #we do this to get the name of the genome name in the database so we can use it to cycle through all of the amr genes
    for indexer in data:
        #cycle through every marker in labels (eg AMR), reset pan_index so that every time we get a new amr we cycle through every pan region

        for marker in labels[indexer]:
            #cycle through every pangenome region
            pan_index = 0
            #cycle through every pan region
            for count in data[indexer]:
                #cycle through ever genome

                for genome in data:

                    if data[genome][pan_index] and labels[genome][amr_index]:
                        pos[0] = pos[0] + 1
                    elif labels[genome][amr_index]:
                        pos[1] = pos[1] + 1
                    elif data[genome][pan_index]:
                        neg[0] = neg[0] + 1
                    else:
                        neg[1] = neg[1] + 1

                p = stats.fisher_exact([pos, neg])
                #p_matrix.append(p)


                if amr_index == 0:
                    p_matrix.append([p])
                else:
                    p_matrix[pan_index].append(p)


                neg = [0, 0]
                pos = [0, 0]

                pan_index = pan_index + 1
                print(pan_index)
            amr_index = amr_index + 1
            print('----------------------------------------------------------------------------------------')
            print(amr_index)
            print('----------------------------------------------------------------------------------------')
        break
    #reject, p = multipletests(p_matrix, alpha=0.05, method='fdr_bh')
    return p_matrix

