import subprocess
import rdflib
import sys
import shutil
from app.modules.PanPredic.definitions import ROOT_DIR
from SPARQLWrapper import SPARQLWrapper, JSON


args = 'perl lib/panseq.pl settings.txt'

def panseq(query_dict):

    novel_config = query_dict['novel']
    match_config = str(query_dict['match'])

    #run panseq to find novel pangenome regions
    #novel = subprocess.Popen(["perl", "/home/james/Panseq/lib/panseq.pl", novel_config], stdout=sys.stdout)
    #novel.communicate()

    # append these pangenome regions to current pangenome fastareference
    #join_files(ROOT_DIR + '/PanGenomeRef/coreGenomeFragments.fasta', match_config)

    #finds a full set of pangenome regions for the queried genomes
    match = subprocess.Popen(["perl", "/home/james/Panseq/lib/panseq.pl", match_config], stdout=sys.stdout)
    match.communicate()



#joins two files together
def join_files(file1, file2):
    """
    :param :
       two text files
    :return: 
        a single text file with the second appended to the first
    """

    #read file to append it to next file
    second = open(file2, "r")
    data = second.read()
    second.close()

    #append second file to the first
    first = open(file1, "a")
    first.write(data)
    first.close()



#queries database and builds a pangenome
def build_pan():
    g = rdflib.Graph()

    # ... add some triples to g somehow ...
    g.parse("some_foaf_file.rdf")

    qres = g.query(
        """SELECT DISTINCT ?aname ?bname
           WHERE {
              ?a foaf:knows ?b .
              ?a foaf:name ?aname .
              ?b foaf:name ?bname .
           }""")

    for row in qres:
        print("%s knows %s" % row)