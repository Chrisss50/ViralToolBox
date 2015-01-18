
import subprocess
import os
import sys
import time

def addtext(label, txt):
    # Add status to label
    currentLabelText = label['text']
    currentLabelText += txt + '\n'
    # Writing it on the label
    label.config(text = currentLabelText)


def checkargs(args,error,label):
    # Check script is run correctly
    addtest(label,"Checking parameters")
    if len(args) < 4:
        error.write("ERROR: Incorrect usage, not enough parameters\nUsage:\
                    python msa_phylip.py infile  err label")
        sys.exit(1)
    # Input file  must exist and be in the running directory'
    if os.path.isfile(args[1]):
        # input file must be named 'infile'
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

def checkphylip(error,label):
    # Check that the necessary programs exit
    addtext(label,"Checking phylip is installed")
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

def runphylogeny(error,label):
    #Run phylogenetic inference
    addtext(label,"Running phylip")
    addtext(label,"Running dnadist")
    start = time.time()
    # Compute a distance matrix from the MSA
    proc = subprocess.Popen(["dnadist"],\
           stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input='y')[0]
    end = time.time()
    total = end - start
    text = "distance matrix computed in "+str(total)+" seconds"
    addtext(label,text)
    # Change name of infile 
    flag = subprocess.call("mv infile msa.fasta",shell=True,stdout=subprocess.PIPE)
    if flag:
        error.write("ERROR: Can't change filename")
        sys.exit(1)
    else:
        # CHange name of distance matrix to infile for neighbor joining
        flag = subprocess.call("mv outfile infile",shell=True,stdout=subprocess.PIPE)
        if flag:
            error.write("ERROR: Can't change filename")
            sys.exit(1)
        else:
            pass
    
    addtext(label,"Running neighbor joining algorithm")
    start = time.time()
    # Compute tree with neighbor joining algorithm
    proc = subprocess.Popen(["neighbor"],\
           stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input='y')[0]
    end = time.time()
    total = end - start
    text = "Neighbor joining tree computed in "+str(total)+" seconds"
    addtext(label,text)
    # Change name of infile to distance_matrix
    flag = subprocess.call("mv infile distance_matrix.txt",shell=True,\
                           stdout=subprocess.PIPE)
    if flag:
        error.write("ERROR: Can't change filename")
        sys.exit(1)
    else:
        # Change name of outfile 
        flag = subprocess.call("mv outfile neighbor.out",shell=True,\
                               stdout=subprocess.PIPE)
        if flag:
            error.write("ERROR: Can't change filename")
            sys.exit(1)
        else:
            # Change name of output tree
            flag = subprocess.call("mv outtree nj.tree",shell=True,\
                                   stdout=subprocess.PIPE)
            if flag:
                error.write("ERROR: Can't change filename")
                sys.exit(1)
            else:
                # Rename the MSA file to infile for further analysis
                flag = subprocess.call("mv msa.fasta infile",shell=True,\
                                       stdout=subprocess.PIPE)
                if flag:
                    error.write("ERROR: Can't change filename")
                    sys.exit(1)

    addtext(label,"Running maximum likelyhood algorithm")
    start = time.time()
    # Compute maximum likelyhood tree
    proc = subprocess.Popen(["dnaml"],\
           stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input='y')[0]
    end = time.time()
    total = end - start
    text = "ML tree computed in "+str(total)+" seconds"
    addtext(label,text)
    # Rename outputs to informative names
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

    addtext(label,"Running maximum parsimony tree algorithm")
    start = time.time()
    # Compute maximum parsimony tree
    proc = subprocess.Popen(["dnapars"],\
           stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input='y')[0]
    end = time.time()
    total = (end - start) / float(60)
    text = "MP trees computed in "+str(total)+" minutes"
    addtext(label,text)
    # Rename outputs to informative names
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
    return None
    
def mpconsense(error,label):
    # From all trees obtained with maximum parsimony algorithm, obtainconsensus
    addtext(label,"Obtaining MP consensus tree")
    # Rename MP tree to intree for analysis
    flag = subprocess.call("mv mp.tree intree",shell=True,\
                           stdout=subprocess.PIPE)
    if flag:
        error.write("ERROR: Can't change filename")
        sys.exit(1)
    
    start = time.time()
    # Obtain consensus of tree
    proc = subprocess.Popen(["consense"],\
                            stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input='y')[0]
    end = time.time()
    total = end - start
    text = "MP consensus tree computed in "+str(total)+" seconds"
    addtext(label,text)
    # Remove and rename files to informative names
    flag = subprocess.call("rm intree outfile",shell=True,\
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
    return None

def getconsensus(error,label):
    # Get consensus tree among all computed trees
    addtext(label,"Appending trees")
    # Concatenate all tree files into one single file
    flag = subprocess.call("cat nj.tree ml.tree mp.tree > intree",shell=True,\
                    stdout=subprocess.PIPE)
    if flag:
        error.write("ERROR: Can't change filename")
        sys.exit(1)
    else:
        pass

    addtext(label,"Computing consensus tree")
    start = time.time()
    # Obtain consensus
    proc = subprocess.Popen(["consense"],\
                            stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate(input="y")[0]
    end = time.time()
    total = end - start
    text = "Consensus tree created in "+str(total)+"seconds")
    addtext(label,text)
    # Rename output to informative name
    flag = subprocess.call("mv outtree ftree.tree",shell=True,\
                           stdout=subprocess.PIPE)
    if flag:
        error.write("Error: Can't change filename")
    else:
        flag = subprocess.call("rm intree outfile",shell=True,\
                           stdout=subprocess.PIPE)
        if flag:
            error.write("Can't delete files")
    return None

def drawtrees(error,label):
    # Generate graphical representation of all trees.
    addtext(label,"Drawing trees")i
    # Import tree drawing modules
    import ete2
    import re
    start = time.time()
    # Trees to draw
    files = ["ml.tree","mp.tree","nj.tree","ftree.tree"]
    filehs = []
    # Loop over filenames and render image
    for tfile in files:
        try:
            handl = open(tfile,'r')
            tree = ete2.Tree(handl.read())
            name = re.sub('.tree','',tfile)
            tree.render(name+'.png')
        except IOError:
            error.write("File: "+tfile+" not found")
            sys.exit(1)
    end = time.time()
    total = end - start
    text = "All trees drawn in "+str(total)+" seconds"
    addtext(text)
    return None
