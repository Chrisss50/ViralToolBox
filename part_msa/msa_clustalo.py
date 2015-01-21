#! /usr/bin/python
import sys
import msa_functions
import os


if __name__ == "__main__":
    # Error log
    r, err = os.pipe()
    err = os.fdopen(err, 'w')
    # Check the script was ran correctly
    msa_functions.checkargs(sys.argv,err,label)
    fastafile = sys.argv[1]
    outpath = sys.argv[2]
    # Check wether clustal is installed
    msa_functions.checkclustal(err,label)
    # Check input is correctly formated
    msa_functions.checkfasta(fastafile,err,label) 
    # Run clustal
    msa_functions.runclustal(fastafile,outpath,err,label)



