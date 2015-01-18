import sys
import os
import requests


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


# To find domains in the given protein sequences this module queries the
# pfam database (http://pfam.xfam.org/) over the RESTful interface
# (http://pfam.xfam.org/help#tabview=tab10).


# Find domains in the proteins. To do so query the pfam database over the
# RESTful interface.
# How the interface works is described here:
# http://pfam.xfam.org/help#tabview=tab10 -> Sequence searching

# http://docs.python-requests.org/en/latest/user/quickstart/
# -> More complicated POST requests, the first one

# Response status code:
# r = requests.get('http://httpbin.org/get')    
# r.status_code
def queryDomains(sequence): 
    #
    formular = {"seq":seq}
    r = requests.post("http://pfam.xfam.org/search/sequence", data=formular)
    print r.text




if __name__ == "__main__":
    # path to the fasta input file (a protein)
    path = sys.argv[1]
    # Read the input file
    headers, seqs = readFasta(path)
    # We have just one sequence
    seq = seqs[0]
    # Query pfam to get the domains in the protein
    queryDomains(seq)