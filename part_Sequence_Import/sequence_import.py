#####################################################################

# Edgar Olijar
# sequence_import.py

import re
import ntpath
from Bio import SeqIO
from Bio import Entrez

#####################################################################

# GET SEQUENCE FROM DATABASE (NCBI)

# Get sequence from NCBI's Entrez databases
# Output of this function is of class:
# <class 'Bio.SeqRecord.SeqRecord'>
# The input file must contain only 1 gene ID 
# input type: string/integer.
# 'err' is an error file
def inputFromDB(geneID,err):
    # convert 'geneID' to string
    geneID = str(geneID)
    # check if geneID contains only numbers:
    if(not bool(re.match("^[0-9]+$",geneID))):
        tmp = "Error in function 'inputFromDB'. "
        tmp += "Variable 'geneID' contains wrong characters. "
        tmp += "Gene ID must be a number."
        # write error message to error file
        err.write(tmp)
    # try to download the sequence from database
    try:
        handle = Entrez.efetch(db="nuccore",id=geneID,rettype="gb",retmode="text")
    except ValueError, e:
        # write error message to error file
        err.write("Error in function 'inputFromDB'. " + str(e))
    # get sequence (class 'Bio.SeqRecord.SeqRecord')
    try:
        SeqRecord = SeqIO.read(handle, "genbank")
    except ValueError, e:
        # write error message to error file
        handle.close()
        err.write("Error in function 'inputFromDB'. "+str(e))
    handle.close()
    # close the error file
    err.close()
    return SeqRecord

#####################################################################

# GET SEQUENCE FROM FILE

# Get path to fasta file and return a sequence.
# Output of this function is of class:
# <class 'Bio.SeqRecord.SeqRecord'>
# The input file must contain only 1 sequence.
# 'err' is an error file
def inputFromFile(filePath,err):
    # Check if file was chosen
    if(filePath == None):
        # write error message to error file
        err.write("Error in function 'inputFromFile'. Empty file path.")
    # get file name and file extension. 
    # I use here module 'ntpath' to get file name, 
    # because it is more system independent than module 'os'.
    fileName, fileExtension = ntpath.splitext(filePath)
    if(fileName == ""):
        # write error message to error file
        err.write("Error in function 'inputFromFile'. No file was chosen.")
    # check if 'fileName' has the correct extension.
    # Allowed are: '.txt', '.fa', '.fasta'
    fileExtensions = ['.txt', '.fa', '.fasta']
    if(fileExtension not in fileExtensions):
        # write error message to error file
        tmp = "Error in function 'inputFromFile'. Wrong file selected. "
        tmp += "Allowed file extensions are: '.txt', '.fa', '.fasta'."
        err.write(tmp)
    # check if imput file is empty
    if(ntpath.getsize(filePath) == 0):
        # write error message to error file
        err.write("Error in function 'inputFromFile'. Input file is empty.")
    # try to open the file
    try:
        handle = open(filePath, "rU")
    except ValueError, e:
        # write error message to error file
        err.write("Error in function 'inputFromFile'. " + str(e))
    # 'SeqIO.read' will check the fasta file syntax.
    # If syntax is wrong, then it will return
    # one of the error messages from below (not all listed here):
    # *** 'More than one record found in handle'
    # *** 'No records found in handle'
    # All 'SeqIO' error messages can be found here:
    # http://biopython.org/DIST/docs/api/Bio.SeqIO-pysrc.html
    # http://biopython.org/DIST/docs/api/Bio.SeqIO-module.html
    try:
        SeqRecord = SeqIO.read(filePath, "fasta")
    except ValueError, e:
        # write error message to error file
        handle.close()
        err.write("Error in function 'inputFromFile'. "+str(e))
    handle.close()
    # check if sequence contains wrong characters.
    # the sequence have to be an RNA (aminoacids)
    # or DNA (nucleotides)
    sequence = str(SeqRecord.seq)
    # check sequence length - it have to be > 0
    if(len(sequence) == 0):
        # write error message to error file
        tmp = "Error in function 'inputFromFile'. "
        tmp += "Sequence has length 0."
        err.write(tmp)
    # is it a DNA ?
    if(bool(re.match("[ACGT]+", sequence))):
        return SeqRecord
    # is it a RNA ?
    if(bool(re.match("[ACGU]+", sequence))):
        return SeqRecord
    else:
        tmp = "Error in function 'inputFromFile'. "
        tmp += "Sequence contains wrong characters."
        # write error message to error file
        err.write(tmp)
    # close the error file
    err.close()

#####################################################################

# CHECK SEQUENCE SIZE

# check size of the sequence
# maxSeqSize = max allowed size of the sequence
def checkSeqSize(seq,maxSeqSize,err):
    # sequence have to be of type string
    if(type(seq) != str):
        # write error message to error file
        tmp = "Error in function 'checkSeqSize'. "
        tmp += "Variable 'seq' must be a string."
        err.write()
    if(len(seq) == 0):
        # write error message to error file
        tmp = "Error in function 'checkSeqSize'. "
        tmp += "Sequence 'seq' has length 0."
        err.write(tmp)
    if(seqSize > maxSeqSize):
        tmp = "Error in function 'checkSeqSize'. "
        tmp += "Sequence 'seq' is too long. "
        tmp += "Sequence size is: "+str(len(seq))+". "
        tmp += "Max allowed sequence size is: "+str(maxSeqSize)+"."
        # write error message to error file
        err.write(tmp)
    # close the error file
    err.close()