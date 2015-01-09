
import subprocess
import os
import sys
from Bio import SeqIO as seqio

def checkargs(args):
    print "Checking parameters"
    if len(args) < 3:
        print "ERROR: Incorrect usage, not enough parameters\n" \
              "Usage: python msa_clustalo.py <fastai input> <output file name>"
        sys.exit(1)

    if os.path.isfile(args[1]):
        pass
    else:
        print "ERROR:",args[1],"could not be found."
        sys.exit(1)
    if os.path.isfile(args[2]):
        print "ERROR",args[2],"already exists."
        sys.exit(1)
    else:
        pass
    return None

def checkclustal():
    DEVNULL = open(os.devnull,'wb')
    flag = subprocess.call("which clustalo", shell=True, stdout=DEVNULL)
    if flag:
        print "ERROR: clustalo could not be found, be shure to have it " \
              "installed http://www.clustal.org/omega/\nor that it is i" \
              "ncluded in your PATH"
        sys.exit(1)
    else:
        return None

def checkfasta(fastafile):
    print "Checking",fastafile,"is valid"
    seqs = seqio.parse(fastafile,'fasta')
    flag = 0
    for seq in seqs:
        if len(seq.seq) <= 0:
            print "ERROR: Sequence",seq.id,"has 0 residues"
            sys.exit(1)
        for nuc in str(seq.seq):
            if nuc not in ['A','C','G','T','a','g','c','t','N']:
                print "ERROR: In sequence",seq.id,"nucleotide not " \
                      "recognized got",nuc,"instead."
                sys.exit(1)
        flag += 1
    if not flag:
        print "ERROR: File",fastafile,"is not a fasta file"
        sys.exit(1)
    else:
        return None

def runclustal(fastafile,outfile):
    print "Running: clustalo -i",fastafile,"-o",outfile
    proc = subprocess.Popen(["clustalo","-i",fastafile,"-o",outfile,
                             "--outfmt","phy","-v"],stdout=subprocess.PIPE)
    res =  proc.communicate()
    print res[0]
