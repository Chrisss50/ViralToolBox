
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
    programs = ["dnadist","dnaml","dnapars","neighbor","consense"]
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
            flag = subprocess.call("mv outtree nj.tree",shell=True,\
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
    
def mpconsense(error):
    print "Obtaining MP consensus tree"
    flag = subprocess.call("mv mp.tree intree",shell=True,\
                           stdout=subprocess.PIPE)
    if flag:
        error.write("ERROR: Can't change filename")
        sys.exit(1)
    
    start = time.time()
    proc = subprocess.Pipie(["consense"],\
                            stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input='y')[0]
    end = time.time()
    total = end - start
    print "MP consensus tree computed in",total,"seconds"
    flag = subpreocess.call("rm intree outfile",shell=True,\
                            stdout=subprocess.PIPE)
    if flag:
        error.write("ERROR: Can't delete files")
        sys.exit(1)
    else:
        flag = subprocess.call("mv outtree mp.tree",shell=True,\
                               stdout=subprocess.PIPE)
        if flag:
            error.write("ERROR: Can't change filename")
            sys.exit(1)

def getconsensus(error):
    print "Appending trees"
    flag = subprocess.call("cat nj.tree ml.tree mp.tree > intree",shell=True,\
                    stdout=subprocess.PIPE)
    if flag:
        error.write("ERROR: Can't change filename")
        sys.exit(1)
    else:
        pass

    print "Computing consensus tree"
    start = time.time()
    proc = subprocess.Popen(["consense"],\
                            stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input="y")[0]
    end = time.time()
    total = end - start
    print "Consensus tree created"
    flag = subprocess.call("mv outtree ftree.tree",shell=True,\
                           stdout=subprocess.PIPE)
    if flag:
        error.write("Error: Can't change filename")
    else:
        flag = subprocess.call("rm intree outfile",shell=True,\
                           stdout=subprocess.PIPE)
        if flag:
            error.write("Can't delete files")

def drawtrees(error):
    import ete2
    import re
    files = ["ml.tree","mp.tree","nj.tree","ftree.tree"]
    filehs = []
    for tfile in files:
        try:
            handl = open(tfile,'r')
            tree = ete2.Tree(handl.read())
            name = re.sub('.tree','',tfile)
            tree.render(name+'.png')
        except IOError:
            error.write("File: "+tfile+" not found")
            sys.exit(1)
