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
    return query

#used to check the presence of pangenome regions within blazegraph
@tolist
@submit
@prefix
def check_panseq():
    '''
    Grabs all objectids having the relation.
    '''
    query = """
    SELECT ?p ?s WHERE {{
          	?p a :PanGenomeRegion .
   			?p g:DNASequence ?s .

    }}
    LIMIT 1
    """
    return query


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

    return query



@tolist
@submit
@prefix
def get_sequences(seq):
    '''
    Grabs all objectids having the relation.
    '''
    query = """
    SELECT ?p WHERE {{
          	?p a :PanGenomeRegion .
   			?p g:DNASequence '{seq}'.

    }}
    """.format(seq = seq)

    return query

#checks to see if a genome is in blazegraph
@tolist
@submit
@prefix
def check_genome(genome):
    '''
    Grabs all objectids having the relation.
    '''
    query = """
    SELECT ?p WHERE {{
          	<{genome}> (:hasPart|:isFoundIn) ?p .
   			?p g:DNASequence '{genome}'.

    }}
    LIMIT 1
    """.format(genome = gu(genome))

    return query