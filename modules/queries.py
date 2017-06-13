import config
from os import path
import sys
sys.path.append(path.abspath('/home/james/backend/app/'))
from app.modules.groupComparisons.decorators import submit, tolist, prefix
from app.modules.turtleGrapher.turtle_utils import generate_uri as gu



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

# gets pangenomeregions for a single genome
@tolist
@submit
@prefix
def get_pangenome(genome):
    '''
    Grabs all objectids having the relation.
    '''
    query = """
    SELECT ?p WHERE {{
          	?p a :PanGenomeRegion .
   			?p :isFoundIn <{genome}> .

    }}
    """.format(genome = gu(genome))
    print(query)
    return query


@tolist
@submit
@prefix
def get_genomes(pan):
    '''
    Grabs all objectids having the relation.
    '''
    query = """
    SELECT ?p WHERE {{
          	?p a g:Genome .
   			?p :hasPart <{PanGenomeRegion}> .

    }}
    """.format(PanGenomeRegion = pan)
    print(query)
    return query


@tolist
@submit
@prefix
def get_virulence(genome):
    '''
    Grabs all objectids having the relation.
    '''
    query = """
    SELECT ?p WHERE {{
          	?p a :VirulenceFactor .
   			?p :isFoundIn <{genome}> .

    }}
    """.format(genome = genome)
    print(query)
    return query