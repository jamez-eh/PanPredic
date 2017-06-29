import config
from os import path
import sys
sys.path.append(path.abspath('/home/james/backend/app/'))
from app.modules.groupComparisons.decorators import submit, tolist, prefix, todict
from app.modules.turtleGrapher.turtle_utils import generate_uri as gu


#TODO: Refactor queries so there are fewer of them and they accept arguments
#queries database and builds a pangenome


#used to check the presence of pangenome regions within blazegraph
@tolist
@submit
@prefix
def check_panseq():
    '''
    '''
    query = """
    SELECT ?p WHERE {{
          	?p a :PanGenomeRegion .

    }}
    LIMIT 1
    """
    return query

@tolist
@submit
@prefix
def query_panseq():
    '''
    '''
    query = """
    SELECT ?p ?s WHERE {{
          	?p a :PanGenomeRegion .
   			?p g:DNASequence ?s .

    }}
    """
    return query


@tolist
@submit
@prefix
def pan_names():
    '''
    '''
    query = """
    SELECT ?p  WHERE {{
          	?p a :PanGenomeRegion .

    }}

    """
    return query

#returns a list of genomes and panregions:
@todict
@submit
@prefix
def gen_pan():
    query = """
    SELECT ?g ?p WHERE {{
            ?g a g:Genome .
          	?p a :PanGenomeRegion .
          	?p :isFoundIn ?g .
    }}
    """
    return query


# gets pangenomeregions for a single genome
@tolist
@submit
@prefix
def get_pangenome(genome):

    query = """
    SELECT ?p WHERE {{
          	?p a :PanGenomeRegion .
   			?p :isFoundIn <{genome}> .

    }}
    """.format(genome = gu(genome))
    return query


#gets genomes that a specific pan region belong to
@tolist
@submit
@prefix
def get_genomes(region):

    query = """
    SELECT ?p WHERE {{
          	?p a g:Genome .
   			?p :hasPart <{region}> .

    }}
    """.format(region = region)
    return query


@tolist
@submit
@prefix
def get_virulence(genome):

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


@todict
@submit
@prefix
def get_virulence():

    query = """
    SELECT ?g ?p WHERE {{
          	?p a :VirulenceFactor .
          	?g a g:Genome .
   			?p :isFoundIn ?g .

    }}
    """

    return query

@tolist
@submit
@prefix
def vir_names():
    '''
    Grabs all Virulence factors possible
    '''
    query = """
    SELECT ?p WHERE {{
          	?p a :VirulenceFactor .

    }}

    """
    return query

@todict
@submit
@prefix
def get_virulence():

    query = """
    SELECT ?g ?p WHERE {{
          	?p a :VirulenceFactor .
          	?g a g:Genome .
   			?p :isFoundIn ?g .

    }}
    """

    return query