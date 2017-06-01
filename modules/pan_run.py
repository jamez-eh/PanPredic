import subprocess
import sys


args = 'perl lib/panseq.pl settings.txt'

def panseq():

    pipe = subprocess.Popen(["perl", "/home/james/Panseq/lib/panseq.pl", "/home/james/pan_genome/PanPredic/panseq_findnew_pangenome.conf"], stdout=sys.stdout)

    pipe.communicate()

    

panseq()