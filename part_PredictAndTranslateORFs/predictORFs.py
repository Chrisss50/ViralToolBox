import sys
import os

__author__ = 'Felix Bartusch'


# Read a fasta file from disk. Trim all whitespaces of the
# sequences. This function returns two lists:
# First list: headers
# Second list: sequences
def readFasta(path, w):
    # Open the file
    try:
        f = open(path, 'r')
        seq = ""
        seqs = []
        headers = []
        # Read the file line for line. It is assumed, that a new
        # sequenced is started by a header.
        seq_num = -1  # the number of the actual sequence
        for line in f:
            if line[0] == ">":
                # If we haven't read the first sequence, we cannot append sth.
                if seq_num != -1:
                    # a new sequence begins, save the read sequence
                    seqs.append(seq.replace("\n", ""))
                seq_num += 1
                seq = ""
                headers.append(line.replace("\n", ""))
            else:
                seq += line
        # append the last sequence to the list of sequences
        seqs.append(seq.replace("\n", ""))
        # Delete all newline characters
        return headers, seqs
    except IOError as e:
        w.write("________________")
        w.write("PredictORFs:")
        w.write("\tError while reading file:")
        w.write("\tI/O error({0}): {1}".format(e.errno, e.strerror) + ": " + path)


def addTextToLabel(label, txt):
    # get the current text of the label
    currentLabelText = label['text']
    # Adding your current status of the tool. Do not forget the newline!
    currentLabelText += txt + '\n'
    # Writing it on the label
    label.config(text=currentLabelText)


# Test whether the given sequence is a DNA sequence.
def isDNA(seq):
    # A DNA sequence just contain the four nucleotides A,G,T,C
    for c in seq:
        if str.upper(c) not in ['A', 'G', 'G', 'C']:
            return False
    return True


# Find potential ORFS and return them as list of strings.
# We assume, that we search ORF for eukaryotes, so the start codon is ATG.
def predictORFS_helper(seq):
    orfs = []
    start_orf = 0
    while start_orf < len(seq) - 2:  # sliding window
        orf = {}
        s = seq[start_orf:start_orf + 3]
        if s in ["ATG", "GTG", "TTG", "ATT", "CTG"]:  # found a start codon
            #  search for the stop codon and an ORF longer than 100n
            #print "found start ORF at", start_orf
            for end_orf in range(start_orf + 3, len(seq), 3):
                e = seq[end_orf:end_orf + 3]
                if e in ["TAA", "TAG", "TGA"]:
                    # Is the ORF long enough?
                    if end_orf + 3 - start_orf > 200:
                        orf["start"] = start_orf
                        orf["end"] = end_orf + 3
                        orf["sequence"] = seq[start_orf:end_orf + 3]
                        orfs.append(orf)
                    start_orf = end_orf - 2
                    break
        start_orf += 1  
    return orfs


# Find potential ORFS and return them as list of dicts.
# Each dict contains 'start', 'end' and 'sequence' as keys.
def predictORFS(seq, label, w):
    # Test wheter we have a valid input sequence
    if(seq == None or len(seq) == 0):
        w.write("________________")
        w.write("PredictORFs:")
        w.write("\tNo input sequence.")
    elif not isDNA(seq):
        w.write("________________")
        w.write("PredictORFs:")
        w.write("\tInput sequence is no DNA sequence.")
    addTextToLabel(label, "Starting predicting ORFs ...\n")
    # Search the sequence from both sides.
    orfs = predictORFS_helper(seq)# + predictORFS_helper(seq[::-1])
    if orfs is None or len(orfs) == 0:
        w.write("________________")
        w.write("PredictORFs:")
        w.write("\tNo ORFs found")
    addTextToLabel(label, "Found " + str(len(orfs)) + " ORFs\n")
    # addTextToLabel(label, txt)
    return orfs
