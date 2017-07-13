import os
import re
import config
from Bio import SeqIO
from modules.turtleGrapher.datastruct_savvy import parse_gene_dict
from modules.turtleGrapher.turtle_grapher import generate_graph
from modules.turtleGrapher.turtle_utils import generate_uri as gu
from modules.blazeUploader import upload_graph
from modules.PanPredic.queries import get_single_region
from modules.beautify import beautify

import ast
from modules.PanPredic import pan
import redis
from rq import Queue

redis_url = config.REDIS_URL
redis_conn = redis.from_url(redis_url)
singles_q = Queue('singles', connection=redis_conn)
multiples_q = Queue('multiples', connection=redis_conn,
                    default_timeout=config.DEFAULT_TIMEOUT)

#generates a hash for a file
def generate_hash(filename):

    """
    :param:
        a file 
    :return: 
        sha1 hash
    """

    from hashlib import sha1
    # the 'b' isn't needed less you run this on Windows
    with open(filename, 'rb') as f:
    #  we apply a sort func to make sure the contents are the same,        # regardless of order
        return sha1(str(sorted(f.readlines())).encode('utf-8')).hexdigest()



def get_fasta_header_from_file(filename):
    """
    Gets the first fasta sequence from the file, and returns the fasta header.
    The files should have already been validated as fasta format.

    :param filename: the absolute path of the fasta file
    :return: header
    """

    for record in SeqIO.parse(filename, "fasta"):
        return record.description

def get_genome_name(header):
    """
    Getting the name of the genome by hierarchy. This requires reading the first
    fasta header from the file. It also assumes a single genome per file.

    :param header: The header containing the record.
    :return genomeName: Name of the genome contained in the header.
    """

    re_patterns = (
        # Look for lcl followed by the possible genome name
        re.compile('((?<=lcl\|)[\w\-\.]+)'),

        # Look    for contigs in the wwwwdddddd format
        re.compile('([A-Za-z]{4}\d{2})\d{6}'),

        # Look for a possible genome name at the beginning of the record ID
        re.compile('^(\w{8}\.\d)'),

        # Look for ref, gb, emb or dbj followed by the possible genome name
        re.compile('(ref\|\w{2}_\w{6}|gb\|\w{8}|emb\|\w{8}|dbj\|\w{8})'),

        # Look for gi followed by the possible genome name
        re.compile('(gi\|\d{8})'),


        # Look for name followed by space, then description
        re.compile('^([\w\-\.]+)\s+[\w\-\.]+')
    )

    # if nothing matches, use the full header as genome_name
    genome_name = header
    for rep in re_patterns:
        m = rep.search(header)

        if m:
            genome_name = m.group(1)
            break

    return str(genome_name)


#returns a dictionary of {genome : genomeURI}
def get_URIs(dir):

    hash_dict = {}
    for file in os.listdir(dir):
        header = get_fasta_header_from_file(dir + '/' + file)
        genome_name = get_genome_name(header)
        hash = generate_hash(dir + '/' + file)
        hash_dict[genome_name] = gu(':' + hash)

    return hash_dict

def create_graph(dict):

    graph = generate_graph()
    for region in dict:
        for genomeURI in dict[region]:
            if not get_single_region(genomeURI):
                graph = parse_gene_dict(graph, dict[region][genomeURI], genomeURI, 'PanGenomeRegion')
                upload_graph.upload_graph(graph)
                graph = generate_graph()
            else: print('Pangenome for this genome is already in Blazegraph')



def pan_graph(single_dict, job_id, query_dir, args_dict):

    job_pan = singles_q.enqueue(pan, single_dict, depends_on=job_id)
    dict = ast.literal_eval(job_pan.result)
    graph = generate_graph()
    for region in dict:
        for genomeURI in dict[region]:
            #checks if genome URI already has a pangenome associated, if so we don't need to process it further
            if not get_single_region(genomeURI):
                job_pan_datastruct = multiples_q.enqueue(upload_graph, graph, dict[region][genomeURI], genomeURI, 'PanGenomeRegion', depends_on=job_pan)
                #clears graph
                graph = generate_graph()
            else: print('Pangenome for this genome is already in Blazegraph')

    job_pan_beautify = singles_q.enqueue(beautify, single_dict, query_dir + 'panseq.p', depends_on=job_pan, result_ttl=-1)

def graph_upload(graph, dict, genomeURI, region):
    '''
    bundles two functions together so it queuable
    :param graph: 
    :param dict: 
    :param genomeURI: amr_dict
    :param region: 
    :return: 
    '''
    graph = parse_gene_dict(graph, dict[region][genomeURI], genomeURI, 'PanGenomeRegion')
    upload_graph.upload_graph(graph)


