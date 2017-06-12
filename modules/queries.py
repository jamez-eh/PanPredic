import config
from os import path
import sys
import rdflib
sys.path.append(path.abspath('/home/james/backend/app/'))
from app.modules.groupComparisons.decorators import submit, tolist, prefix
from app.modules.turtleGrapher.turtle_utils import link_uris as gu



blazegraph_url = config.database['blazegraph_url']

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



list = query_panseq()

