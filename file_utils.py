from Bio import SeqIO


def fasta_formatter(dir):
    
    original_file = "./original.fasta"
    corrected_file = "./corrected.fasta"
    for file in os.listdir(dir):
        with open(corrected_file, 'w') as corrected:
            records = SeqIO.parse(original_file, 'fasta')
                for record in records:
                    record.description = 'bar' # <- Add this line
                    SeqIO.write(record, corrected, 'fasta')
