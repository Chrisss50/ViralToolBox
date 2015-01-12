
import subprocess
import os
import sys
import time

def checkargs(args,error):
    if len(args) < 2:
        error.write("ERROR: Incorrect usage, not enough parameters\nUsage:\
                    python msa_clustalo.py <fasta input>")
        sys.exit(1)

    if os.path.isfile(args[1]):
        if args[1] != 'infile':
            error.write("ERROR: Input file must be named \"infile\"")
            error.close()
            sys.exit(1)
        else:
            pass
    else:
        error.write("ERROR: Input file \"infile\" could not be detected")
        error.close()
        sys.exit(1)
    return None

def checkphylip(error):
    DEVNULL = open(os.devnull,'wb')
    programs = ["dnadist","dnaml","dnapars","neighbor"]
    for program in programs:
        flag = subprocess.call("which "+program, shell=True, stdout=DEVNULL)
        if flag:
            error.write("ERROR: "+program+" could not be found, be shure to"\
                        "have it installed http://evolution.genetics.washington.edu"\
                        "phylip.html\nor that it is included in your PATH")
            sys.exit(1)
    else:
        return None

def runphylogeny(error):
    print "Running dnadist"
    start = time.time()
    proc = subprocess.Popen(["dnadist"],\
           stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input='y')[0]
    end = time.time()
    total = end - start
    print "distance matrix computed in",total,"seconds"
    flag = subprocess.call("mv infile msa.fasta",shell=True,stdout=subprocess.PIPE)
    if flag:
        error.write("ERROR: Can't change filename")
        sys.exit(1)
    else:
        flag = subprocess.call("mv outfile infile",shell=True,stdout=subprocess.PIPE)
        if flag:
            error.write("ERROR: Can't change filename")
            sys.exit(1)
        else:
            pass
    
    print "Running neighbor joining algorithm"
    start = time.time()
    proc = subprocess.Popen(["neighbor"],\
           stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input='y')[0]
    end = time.time()
    total = end - start
    print "Neighbor joining tree computed in",total,"seconds"
    flag = subprocess.call("mv infile distance_matrix.txt",shell=True,\
                           stdout=subprocess.PIPE)
    if flag:
        error.write("ERROR: Can't change filename")
        sys.exit(1)
    else:
        flag = subprocess.call("mv outfile neighbor.out",shell=True,\
                               stdout=subprocess.PIPE)
        if flag:
            error.write("ERROR: Can't change filename")
            sys.exit(1)
        else:
            flag = subprocess.call("mv outtree neighbor.tree",shell=True,\
                                   stdout=subprocess.PIPE)
            if flag:
                error.write("ERROR: Can't change filename")
                sys.exit(1)
            else:
                flag = subprocess.call("mv msa.fasta infile",shell=True,\
                                       stdout=subprocess.PIPE)
                if flag:
                    error.write("ERROR: Can't change filename")
                    sys.exit(1)

    print "Running maximum likelyhood algorithm"
    start = time.time()
    proc = subprocess.Popen(["dnaml"],\
           stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input='y')[0]
    end = time.time()
    total = end - start
    print "ML tree computed in",total,"seconds"
    flag = subprocess.call("mv outtree ml.tree",shell=True,\
                                       stdout=subprocess.PIPE)
    if flag:
        error.write("ERROR: Can't change filename")
        sys.exit(1)
    else:
        flag = subprocess.call("mv outfile ml.out",shell=True,\
                                       stdout=subprocess.PIPE)
        if flag:
            error.write("ERROR: Can't change filename")
            sys.exit(1)

    print "Running maximum parsimony tree algorithm"
    start = time.time()
    proc = subprocess.Popen(["dnapars"],\
           stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input='y')[0]
    end = time.time()
    total = (end - start) / float(60)
    print "MP trees computed in",total,"minutes"
    flag = subprocess.call("mv outtree mp.tree",shell=True,\
                                       stdout=subprocess.PIPE)
    if flag:
        error.write("ERROR: Can't change filename")
        sys.exit(1)
    else:
        flag = subprocess.call("mv outfile mp.out",shell=True,\
                                       stdout=subprocess.PIPE)
        if flag:
            error.write("ERROR: Can't change filename")
            sys.exit(1)

