from datetime import datetime
import pdb
from Bio import SeqIO
import subprocess
from os.path import basename
import re
import os
from modules.turtleGrapher.turtle_utils import generate_uri as gu
from modules.turtleGrapher.turtle_utils import slugify
from modules.PanPredic.definitions import ROOT_DIR


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

    
def contig_name_parse(pan_contig):
    """
    The panseq contig name is unhelpful
    :param:
        a contig named by panseq
    :return: 
        the basename of the contig
    """
    pan_contig = re.sub('[|]', '', pan_contig)

    if re.search('(.*?)(?=_E)', pan_contig):
        #m = re.search('(?<=\|)(.*?)(?=_E)', pan_contig)
        m = re.search('(.*?)(?=_E)', pan_contig)
        #m = re.search('(?<=\|).+', m.group(0))

    #elif re.search('(?<=\|).+', pan_contig):
        #m = re.search('(?<=\|).+', pan_contig)
        #m = re.search('(?<=\|).+', m.group(0))

    else:
        return pan_contig

    return m.group(0)


def get_URIs(dir):
    '''
    param: dir: a directory of fasta files for which we want to generate a hash for each and prepend a ':'
    return: hash_dict: a dict in form {genome_name: :A56349fdBafaBCDaq4905834}
    '''

    hash_dict = {}
    for file in os.listdir(dir):
        header = get_fasta_header_from_file(dir + '/' + file)
        genome_name = slugify(get_genome_name(header))
        hash = generate_hash(dir + '/' + file)
        hash_dict[genome_name] = ':' + hash

    return hash_dict


def get_fasta_header_from_file(filename):
    """
    Gets the first fasta sequence from the file, and returns the fasta header.
    The files should have already been validated as fasta format.

    :param filename: the absolute path of the fasta file
    :return: header
    """

    for record in SeqIO.parse(filename, "fasta"):
        print(record.description)
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
    print header
    for rep in re_patterns:
        m = rep.search(header)

        if m:
            genome_name = m.group(1)
            break

    return str(genome_name)



def tagger(dir, tag, dst):
    '''
    params: dir: directory of fasta files with header to alter
    params: tag: if it is a positive or negative tag
    '''

    for original_file in os.listdir(dir):
        if original_file.endswith('.fna') or original_file.endswith('.fasta'):

            current_file = dir + '/' + original_file
            genome_name = basename(current_file)
            genome = os.path.splitext(genome_name)[0]
        
            original, edit = open(dir + '/' + original_file), open(dst + '/'  + genome +  '.fasta', 'w+')

            contig_index = 1

            for line in original:
                if line.startswith('>'):
                    newname= '>lcl|' + genome + tag+ '|contig' + str(contig_index)  +'\n'
                    edit.write(newname)
                    contig_index = contig_index + 1
                else:
                    edit.write(line)
            
            original.close()
            edit.close()
    

def dir_merge(dir_one, dir_two):
    '''
    merges two directories into a list of all the files
    '''

    return os.listdir(dir_one) + os.listdir(dir_two)


#TODO: add src to definitions and dst to definitions
def sym_linker(file_list, dst):
    '''
    Creates a subdirectory in the query directory with symlinks to all the fasta files, 
    necessary for panseq to run with all the junk that other process place in the query dir
    :param a list of files
    :param dst: destination directory
    :return: source directory
    '''
    now = datetime.now()
    now = now.strftime("%Y-%m-%d-%H-%M-%S-%f")

    try:
        os.mkdir(dst)
    except:
        print(dst + ' already exists')


    for file in file_list:
        if file.endswith('.fna') or file.endswith('.fasta'):
            try:
                os.symlink(file, dst + '/' + os.path.basename(file))
            except:
                print(dst + '/' + file +' already exists')


    return dst

