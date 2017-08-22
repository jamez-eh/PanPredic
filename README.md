# PanPredic

## Use:

   PanPredic is divided into two modules;

   One is a collection of scripts for the integration of [Panseq](https://github.com/chadlaing/Panseq) into [Spfy](https://github.com/superphy). This runs Panseq and stores the results into a graph database. Functions also exist to acquire presence or absence vectors for a genome(s) to be used further down analysis pipelines. This integration requires no configuration from the user.

   The command line interface runs outside the database. It runs Panseq and makes phenotype predictions based on these results.
   cmd_pan.py takes three arguments:

   - a directory of fasta files positive for a phenotype
   - a directory of fasta files negative for a phenotype
   - a directory of fasta files for which a prediction will be made

   ```
   python cmd_pan.py -p /directory_positive_phenotype -n /directory_negative_phenotype -q /directory_unknown_phenotype
   
   ```

## How it works:

   The command line interface runs panseq on the positive and negative directories and retrieves presence or absence vectors from the Panseq output. A support vector machine is then trained on this output after parameter optimization and feature selection. Panseq is then ran in novel mode with the unknown directory. The output from this Panseq run and the SVM trained are then used to make predictions for each genome.


## Dependencies:

   Panseq
   Sci-Kit Learn
   Pandas
   Numpy
   
   