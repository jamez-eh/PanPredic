from app.modules.PanPredic.modules.queries import gen_pan, pan_names, get_virulence, vir_names


def eval_vectors(gen_pan, pan_genome):
    '''

    :param gen_pan: a dictorary in form {genome: [region, ....], genome:  .........}
    :param pan_genome: a list of all pangenome regions
    :return: vector_dict: a dictionary of genomes with assoc bitmap vector of presence or abscence of a pangenome region 
    '''

    vector_dict = {}

    for genome in gen_pan:

        vector_dict[genome] = []

        for pan in pan_genome:

            if pan in gen_pan[genome]:
                vector_dict[genome].append(1)
            else:
                vector_dict[genome].append(0)

    return vector_dict


def get_labels():
    '''

    :return: a list of all labels for 
    '''

    vir = get_virulence()
    names = vir_names()

    return eval_vectors(vir, names)


def get_data():

    #get a list of genomes and associated pan genome regions
    gen_panreg = gen_pan()
    pan_genome = pan_names()

    return eval_vectors(gen_panreg, pan_genome)
