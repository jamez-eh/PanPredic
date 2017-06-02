import modules.uploader
import pandas as pd
from hashlib import sha1
import os
from definitions import ROOT_DIR




def test_parse_pan():

    df = modules.uploader.parse_pan(ROOT_DIR +'/tests/data/test_pan.txt')
    df.to_csv(ROOT_DIR + '/tests/data/test_parsed.txt', sep='\t', index=False)

    with open(ROOT_DIR + '/tests/data/test_parsed.txt') as f:
        hash = sha1(str(sorted(f.readlines())).encode('utf-8')).hexdigest()


    assert hash == '5ebb7e676a3b606befa0d7ab0fbbf49a149379e0'


def test_pan_to_dict():

    df = pd.read_csv(ROOT_DIR + '/tests/data/test_parsetodict.txt', sep=None)

    pan_dict = modules.uploader.pan_to_dict(df)
    #modules.uploader.json_dump(ROOT_DIR + '/tests/data/test_pan_dict.json', pan_dict)

    test_dict = modules.uploader.json_load(ROOT_DIR + '/tests/data/test_pan_dict.json')
    assert pan_dict == test_dict


def test_get_sequence_dict():

    file = '/tests/data/genome_files/GCA_000091005.1_ASM9100v1_genomic.fna'
    dict = modules.uploader.get_sequence_dict(ROOT_DIR + file )

    test_data = modules.uploader.json_load(ROOT_DIR + '/tests/data/test_sequence_dict.json')

    assert dict == test_data


