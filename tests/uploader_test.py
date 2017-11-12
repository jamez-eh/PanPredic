import modules.PanPredic.uploader as uploader
import pandas as pd
from hashlib import sha1
import os
from modules.PanPredic.definitions import ROOT_DIR


def test_genome_replace():

    hash_dict = {'CAMP0000001.1': ':123412341234', 'CAMP01.1' : 'WRONG'}
    genome = 'CAMP000001'
    genome = uploader.genome_replace(hash_dict, genome)

    print(genome)
