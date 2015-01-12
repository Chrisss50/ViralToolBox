import time
import subprocess
import os
import sys
from Bio import SeqIO as seqio

def checkargs(args,error):
    print "Checking parameters"
    if len(args) < 2:
        error.write("ERROR: Incorrect usage, not enough parameters\nUsage:\
                    python msa_clustalo.py <fasta input>")
        sys.exit(1)

    if os.path.isfile(args[1]):
        pass
    else:
        error.write("ERROR:",args[1],"could not be found.")
        sys.exit(1)
    #if os.path.isfile(args[2]):
    #    error.write("ERROR",args[2],"already exists.")
    #    sys.exit(1)
    #else:
    #    pass
    return None

def checkclustal(error):
    print "Checking clustalo is installed"
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

def runclustal(fastafile,error):
    print "Running: clustalo -i",fastafile,"-o infile"
    start = time.time()
    proc = subprocess.Popen(["clustalo","-i",fastafile,"-o","infile",
                             "--outfmt","phy","-v"])
    res =  proc.communicate()
    end = time.time()
    total = end - start
    print res[0]
    print "MSA computed in",total,"seconds"
