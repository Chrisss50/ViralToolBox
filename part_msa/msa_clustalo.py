#! /usr/bin/python
import sys
import msa_functions

args = sys.argv

def main():
    msa_functions.checkargs(args)
    fastafile = args[1]
    outfile = args[2]
    print "Infile is",fastafile,"\nOutfile is",outfile
    msa_functions.checkclustal()
    msa_functions.checkfasta(fastafile)
    print "Starting clustalo"
    msa_functions.runclustal(fastafile,outfile)



if __name__ == "__main__":
    main()
