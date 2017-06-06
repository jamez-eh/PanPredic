from definitions import ROOT_DIR, PAN_RESULTS, NOVEL_RESULTS




# TODO: edit file locations of programs

def gen_novel(genome_files):

    with open(ROOT_DIR + 'panseq_findnew_pangenome.conf2', 'wb') as f:
        f.writelines([b'queryDirectory   ' + genome_files.encode(),
                    b'referenceDirectory '	+ ROOT_DIR.encode() + b'/PanGenomeRef',
                    b'baseDirectory  ' + NOVEL_RESULTS.encode(),
                    b'numberOfCores	4',
                    b'mummerDirectory	/home/james/pan_genome/PanPredic/MUMmer3.23/',
                    b'blastDirectory	/home/james/pan_genome/PanPredic/ncbi-blast-2.6.0+/bin/',
                    b'minimumNovelRegionSize	500',
                    b'novelRegionFinderMode	no_duplicates',
                    b'muscleExecutable	/home/james/pan_genome/PanPredic/muscle3.8.31_i86linux64',
                    b'percentIdentityCutoff	90',
                    b'runMode	novel',
                    b'overwrite 1'])
        return f


def gen_match(genome_files):
    with open(ROOT_DIR + 'panseq_match_pangenome2.conf', 'wb') as f:
        f.writelines([b'queryDirectory   ' + genome_files.encode(),
                    #'queryFile  ' + ROOT_DIR + '/PanGenomeRef/coreGenomeFragments.fasta',
                    b'baseDirectory  ' +  PAN_RESULTS.encode(),
                    b'numberOfCores	4',
                    b'mummerDirectory	/home/james/pan_genome/PanPredic/MUMmer3.23/',
                    b'blastDirectory	/home/james/pan_genome/PanPredic/ncbi-blast-2.6.0+/bin/',
                    b'minimumNovelRegionSize	500',
                    b'muscleExecutable	/home/james/pan_genome/PanPredic/muscle3.8.31_i86linux64',
                    b'novelRegionFinderMode	no_duplicates',
                    b'muscleExecutable	/home/james/pan_genome/PanPredic/muscle3.8.31_i86linux64',
                    b'fragmentationSize	500',
                    b'percentIdentityCutoff	90',
                    b'runMode	pan',
                    b'nameOrId	name',
                    b'overwrite 1'])
        return f

#driver function generates both necessary conf files
def generate_conf(genome_files):

    query_dict = {}

    query_dict['novel'] = gen_novel(genome_files)
    query_dict['match'] = gen_match(genome_files)

    return query_dict

