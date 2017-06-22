import logging
from modules.loggingFunctions import initialize_logging
import scipy.stats as stats
import pandas as pd
from app.modules.PanPredic.modules.SVM import get_labels, get_data


# logging
log_file = initialize_logging()
log = logging.getLogger(__name__)




def fishers():


    data = get_data()
    labels = get_labels()

    p_matrix = []
    index = 0
    index2 = 0
    pos = [0, 0]
    neg = [0, 0]

    #cycle through every genome
    for indexer in data:
        #cycle through every marker in labels (eg AMR)
        for marker in labels[indexer]:
            #cycle through every pangenome region
            for count in data[indexer]:
                #cycle through ever genome
                for genome in data:

                    if data[genome][index] and labels[genome][index2]:
                        pos[0] = pos[0] + 1
                    elif labels[genome][index2]:
                        pos[1] = pos[1] + 1
                    elif data[genome][index]:
                        neg[0] = neg[0] + 1
                    else:
                        neg[1] = neg[1] + 1

                p = stats.fishers.exact(pos, neg)

                if index2 == 0:
                    p_matrix.append([p])
                else:
                    p_matrix[index].append(p)

                index = index + 1
            index2 = index2 + 1

    return p_matrix

