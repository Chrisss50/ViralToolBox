import sys
import os

__author__ = 'Felix Bartusch'


# Read a fasta file from disk. Trim all whitespaces of the
# sequences. This function returns two lists:
# First list: headers
# Second list: sequences
def readFasta(path):
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
        print "I/O error({0}): {1}".format(e.errno, e.strerror) + ": " + path


# Find potential ORFS and return them as list of strings.
# We assume, that we search ORF for eukaryotes, so the start codon is ATG.
def predictORFS_helper(seq):
    orfs = []
    start_orf = 0
    while start_orf < len(seq) - 2:  #in range(0, len(seq) - 2):    # sliding window
        orf = {}
        s = seq[start_orf:start_orf + 3]
        if s in ["ATG", "GTG", "TTG"]:  # found a start codon
            #  search for the stop codon and an ORF longer than 100n
            for end_orf in range(start_orf + 3, len(seq), 3):
                e = seq[end_orf:end_orf + 3]
                if e in ["TAA", "TAG", "TGA"]:
                    # Is the ORF long enough?
                    if end_orf + 3 - start_orf > 200:
                        orf["start"] = start_orf
                        orf["end"] = end_orf + 3
                        orf["sequence"] = seq[start_orf:end_orf + 3]
                        orfs.append(orf)
                        start_orf += 1
                    break
                #else:
                    #start_orf += 1
        #else:
            #start_orf += 1
        start_orf += 1  
    return orfs


# Find potential ORFS and return them as list of dicts.
# Each dict contains 'start', 'end' and 'sequence' as keys.
def predictORFS(seq, w):
    print "Starting predicting ORFs ..."
    # Search the sequence from both sides.
    orfs = predictORFS_helper(seq) + predictORFS_helper(seq[::-1])
    if orfs is None or len(orfs) == 0:
        w.write("________________")
        w.write("Error-Log of predictORFs:")
        w.write("No ORFs found")
    print "Found", len(orfs), "ORFs"
    print "End predicting ORFs!"
    # Write the orfs to file or return as
    # TODO? Or return just the list
    return orfs


if __name__ == "__main__":
    # path to the fasta input file
    path = sys.argv[1]
    # Read the input file
    headers, seqs = readFasta(path)
    # We have just one sequence
    seq = seqs[0]
    # Predict the ORFs
    w = os.pipe()
    orfs = predictORFS(seq, w)
    # How many ORFs have we found?
    # Print the ORFs
    for orf in orfs:
        print orf