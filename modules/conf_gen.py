from modules.PanPredic.definitions import ROOT_DIR




# TODO: edit file locations of programs

def gen_novel(genome_files):

    with open(ROOT_DIR + 'panseq_findnew_pangenome.conf2', 'wb') as f:
        f.writelines(['queryDirectory   ' + genome_files,
                    'referenceDirectory '	+ ROOT_DIR + '/PanGenomeRef',
                    'baseDirectory  ' + ROOT_DIR + '/novelPanResults',
                    'numberOfCores	4',
                    'mummerDirectory	/home/james/pan_genome/PanPredic/MUMmer3.23/',
                    'blastDirectory	/home/james/pan_genome/PanPredic/ncbi-blast-2.6.0+/bin/',
                    'minimumNovelRegionSize	500',
                    'novelRegionFinderMode	no_duplicates',
                    'muscleExecutable	/home/james/pan_genome/PanPredic/muscle3.8.31_i86linux64',
                    'percentIdentityCutoff	90',
                    'runMode	novel',
                    'overwrite 1'])
        return f


def gen_match(genome_files):
    with open(ROOT_DIR + 'panseq_match_pangenome2.conf', 'wb') as f:
        f.writelines(['queryDirectory   ' + genome_files,
                    #'queryFile  ' + ROOT_DIR + '/PanGenomeRef/coreGenomeFragments.fasta',
                    'baseDirectory  ' + ROOT_DIR + '/novelPanResults',
                    'numberOfCores	4',
                    'mummerDirectory	/home/james/pan_genome/PanPredic/MUMmer3.23/',
                    'blastDirectory	/home/james/pan_genome/PanPredic/ncbi-blast-2.6.0+/bin/',
                    'minimumNovelRegionSize	500',
                    'muscleExecutable	/home/james/pan_genome/PanPredic/muscle3.8.31_i86linux64',
                    'novelRegionFinderMode	no_duplicates',
                    'muscleExecutable	/home/james/pan_genome/PanPredic/muscle3.8.31_i86linux64',
                    'fragmentationSize	500',
                    'percentIdentityCutoff	90',
                    'runMode	pan',
                    'nameOrId	name',
                    'overwrite 1'])
        return f

#driver function generates both necessary conf files
def generate_conf(genome_files):

    query_dict = {}

    query_dict['novel'] = gen_novel(genome_files)
    query_dict['match'] = gen_match(genome_files)

    return query_dict

