
import subprocess
import os
import sys
from Bio import SeqIO as seqio

def checkargs(args,error):
    print "Checking parameters"
    if len(args) < 3:
        error.write("ERROR: Incorrect usage, not enough parameters\nUsage:\
                    python msa_clustalo.py <fastai input> <output file name>")
        sys.exit(1)

    if os.path.isfile(args[1]):
        pass
    else:
        error.write("ERROR:",args[1],"could not be found.")
        sys.exit(1)
    if os.path.isfile(args[2]):
        error.write("ERROR",args[2],"already exists.")
        sys.exit(1)
    else:
        pass
    return None

def checkclustal(error):
    DEVNULL = open(os.devnull,'wb')
    flag = subprocess.call("which clustalo", shell=True, stdout=DEVNULL)
    if flag:
        error.write("ERROR: clustalo could not be found, be shure to have it\
                    installed http://www.clustal.org/omega/\nor that it is\
                    included in your PATH")
        sys.exit(1)
    else:
        return None

def checkfasta(fastafile,error):
    print "Checking",fastafile,"is valid"
    seqs = seqio.parse(fastafile,'fasta')
    flag = 0
    for seq in seqs:
        if len(seq.seq) <= 0:
            error.write("ERROR: Sequence",seq.id,"has 0 residues")
            sys.exit(1)
        for nuc in str(seq.seq):
            if nuc not in ['A','C','G','T','a','g','c','t','N']:
                print "ERROR: In sequence",seq.id,"nucleotide not " \
                      "recognized got",nuc,"instead."
                sys.exit(1)
        flag += 1
    if not flag:
        error.write("ERROR: File",fastafile,"is not a fasta file")
        sys.exit(1)
    else:
        return None

def runclustal(fastafile,outfile,error):
    print "Running: clustalo -i",fastafile,"-o",outfile
    proc = subprocess.Popen(["clustalo","-i",fastafile,"-o",outfile,
                             "--outfmt","phy","-v"],stdout=subprocess.PIPE)
    res =  proc.communicate()
    print res[0]
