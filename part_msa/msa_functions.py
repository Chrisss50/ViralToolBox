import time
import subprocess
import os
import sys
from Bio import SeqIO as seqio

def addtext(label, txt):
    # Add status to label
    currentLabelText = label['text']
    currentLabelText += txt + '\n'
    # Writing it on the label
    label.config(text = currentLabelText)

def checkargs(args,error,label):
    # Check script was run correctly
    addtext(label,"Checking parameters")
    # usage: python msa_clustalo.py <fasta input> err label
    if len(args) < 4:
        error.write("ERROR: Incorrect usage, not enough parameters\nUsage:\
                    python msa_clustalo.py <fasta input> err label")
        return error
    # Input must be a file
    if os.path.isfile(args[1]):
        pass
    else:
        error.write("ERROR:",args[1],"could not be found.")
        return error
    return None

def checkclustal(error,label):
    # Check clostalo is installed and in PATH
    addtext(label,"Checking clustalo is installed")
    # 'which clustalo must exit with status = 0'
    proc = subprocess.Popen("which clustalo", shell=True,
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    res = proc.communicate()
    if res[1] == '':
        pass
    else:
        error.write("ERROR: clustalo could not be found, be shure to have it\
                    installed http://www.clustal.org/omega/\nor that it is\
                    included in your PATH")
        return error
    return None

def checkfasta(fastafile,error,label):
    # Input file must be in fasta format
    text = "Checking "+fastafile+" is valid"
    addtext(label, text)
    # PArse file with Bio.SeqIO.parse
    seqs = seqio.parse(fastafile,'fasta')
    flag = 0
    # Loop over sequences
    for seq in seqs:
        # No empty sequences allowed
        if len(seq.seq) <= 0:
            error.write("ERROR: Sequence",seq.id,"has 0 residues")
            sys.exit(1)
        # Sequences must be DNA
        for nuc in str(seq.seq):
            if nuc not in ['A','C','G','T','a','g','c','t','N']:
                error.write("ERROR: In sequence "+str(seq.id)+" nucleotide"\
                            " not recognized got "+nuc+" instead.")
                return error
        flag += 1
    if not flag:
        error.write("ERROR: File",fastafile,"is not a fasta file")
        return error
    else:
        return None

def runclustal(fastafile,outpath,error,label):
    # Check if path to write output exists
    pathflag = os.path.exists(outpath)
    if pathflag:
        pass
    else:
        error.write("Error: Path " + outpath + "does not exist")
        sys.exit(1)
    writeout = outpath + "infile"
    # print input summary and run clustalo
    text =  "Infile is "+fastafile+"\nOutfile is infile"+\
            "\nRunning: clustalo -i "+fastafile+" -o",writeout,\
            "\nStarting clustalo"
    addtext(label,text)
    start = time.time()
    # Runs clustalo with sequences provided, output format is in phylip
    proc = subprocess.Popen("clustalo "+"-i "+fastafile+" -o "+writeout+
                            " --outfmt "+"phy "+"-v",shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res =  proc.communicate()
    if res[1] == '':
        addtext(label,res[0])
    else:
        error.write(res[1])
        return error
    end = time.time()
    total = end - start
    # Print output of clustalo
    addtext(label,res[0])
    text = "MSA computed in "+str(total)+" seconds"
    addtext(label,text)
    return writeout
