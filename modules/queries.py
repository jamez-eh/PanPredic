import config
from os import path
import sys
sys.path.append(path.abspath('/home/james/backend/app/'))
from app.modules.groupComparisons.decorators import submit, tolist, prefix



#queries database and builds a pangenome
@tolist
@submit
@prefix
def query_panseq():
    '''
    Grabs all objectids having the relation.
    '''
    query = """
    SELECT ?p ?s WHERE {{
          	?p a :PanGenomeRegion .
   			?p g:DNASequence ?s .
       
    }}
    """
    return query


#query the entire pangenome and get


