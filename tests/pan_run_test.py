import pan_run
import shutil
from hashlib import sha1
from definitions import ROOT_DIR
import os



def test_join_files():

    #open test data and store it in a variable so it we can regenerate it
    with open(ROOT_DIR +'/tests/data/test_join1.txt', 'rb') as f:
        data = f.read()

    pan_run.join_files(ROOT_DIR + '/tests/data/test_join1.txt', ROOT_DIR + '/tests/data/test_join2.txt')

    with open(ROOT_DIR + '/tests/data/test_join1.txt') as f:
        hash = sha1(str(f.readlines()).encode('utf-8')).hexdigest()

    assert hash == '3215f389781e18cba60e809c88d9d22185f4d92d'
    #delete new data
    os.remove( ROOT_DIR + '/tests/data/test_join1.txt')

    #regenerate test data
    with open(ROOT_DIR + '/tests/data/test_join1.txt', 'wb') as f:
        f.write(data)


test_join_files()
