#####################################################################

# Edgar Olijar
# sequence_import.py

import re
import ntpath
import datetime
from Bio import SeqIO
from Bio import Entrez

#####################################################################

# GET SEQUENCE FROM DATABASE (NCBI)

# Get sequence from NCBI's Entrez databases
# Output of this function is of class:
# <class 'Bio.SeqRecord.SeqRecord'>
# 'geneID' must contain only 1 gene ID 
# input type: integer.
# 'err' is an error file
def inputFromDB(geneID,err,email):
    # get current time:
    timeStamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    geneID = str(geneID)
    Entrez.email = email
    # try to download the sequence from database
    try:
        handle = Entrez.efetch(db="nuccore",id=geneID,rettype="gb",retmode="text",email)
    except ValueError, e:
        tmp = timeStamp+". Error in function 'inputFromDB'. "+str(e)
        # write error message to error file
        err.write(tmp)
    # get sequence (class 'Bio.SeqRecord.SeqRecord')
    try:
        SeqRecord = SeqIO.read(handle, "genbank")
    except ValueError, e:
        tmp = timeStamp+". Error in function 'inputFromDB'. "+str(e)
        # write error message to error file
        handle.close()
        err.write(tmp)
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
    # get current time
    timeStamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    # Check if file was chosen
    if(filePath == None):
        tmp = timeStamp + ". "
        tmp += "Error in function 'inputFromFile'. Empty file path."
        # write error message to error file
        err.write(tmp)
    # get file name and file extension. 
    # I use here module 'ntpath' to get file name, 
    # because it is more system independent than module 'os'.
    fileName, fileExtension = ntpath.splitext(filePath)
    if(fileName == ""):
        tmp = timeStamp + ". "
        tmp += "Error in function 'inputFromFile'. No file was chosen."
        # write error message to error file
        err.write(tmp)
    # check if 'fileName' has the correct extension.
    # Allowed are: '.txt', '.fa', '.fasta'
    fileExtensions = ['.txt', '.fa', '.fasta']
    if(fileExtension not in fileExtensions):
        tmp = timeStamp + ". "
        tmp += "Error in function 'inputFromFile'. Wrong file selected. "
        tmp += "Allowed file extensions are: '.txt', '.fa', '.fasta'."
        # write error message to error file
        err.write(tmp)
    # check if imput file is empty
    if(ntpath.getsize(filePath) == 0):
        tmp = timeStamp + ". "
        tmp += "Error in function 'inputFromFile'. Input file is empty."
        # write error message to error file
        err.write(tmp)
    # try to open the file
    try:
        handle = open(filePath, "rU")
    except ValueError, e:
        tmp = timeStamp + ". "
        tmp += "Error in function 'inputFromFile'. " + str(e)
        # write error message to error file
        err.write(tmp)
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
        handle.close()
        tmp = timeStamp + ". "
        tmp += "Error in function 'inputFromFile'. "+str(e)
        # write error message to error file
        err.write(tmp)
    handle.close()
    # check if sequence contains wrong characters.
    # the sequence have to be an RNA or DNA
    sequence = str(SeqRecord.seq).upper()
    # check sequence length - it have to be > 0
    if(len(sequence) == 0):
        tmp = timeStamp + ". "
        tmp += "Error in function 'inputFromFile'. "
        tmp += "Sequence has length 0."
        # write error message to error file
        err.write(tmp)
    # is it a DNA ?
    if(bool(re.match("^[ACGT]+$", sequence))):
        return SeqRecord
    # is it a RNA ?
    if(bool(re.match("^[ACGU]+$", sequence))):
        return SeqRecord
    else:
        tmp = timeStamp + ". "
        tmp += "Error in function 'inputFromFile'. "
        tmp += "Sequence contains wrong characters."
        # write error message to error file
        err.write(tmp)
    # close the error file
    err.close()

#####################################################################

# input: object of type '<class 'Bio.SeqRecord.SeqRecord'>'
# output: string (sequence)
def get_sequence_from_SeqRecord(seq_record):
    return seq_record.seq

# CHECK SEQUENCE SIZE

# check size of the sequence
# maxSeqSize = max allowed size of the sequence
def checkSeqSize(seq,maxSeqSize,err):
    # get current time:
    timeStamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    # sequence have to be of type string
    if(type(seq) != str):
        tmp = timeStamp + ". "
        tmp += "Error in function 'checkSeqSize'. "
        tmp += "Variable 'seq' must be a string."
        # write error message to error file
        err.write(tmp)
    if(len(seq) == 0):
        tmp = timeStamp + ". "
        tmp += "Error in function 'checkSeqSize'. "
        tmp += "Sequence 'seq' has length 0."
        # write error message to error file
        err.write(tmp)
    if(seqSize > maxSeqSize):
        tmp = timeStamp + ". "
        tmp += "Error in function 'checkSeqSize'. "
        tmp += "Sequence 'seq' is too long.\n"
        tmp += "Sequence size is: "+str(len(seq))+". "
        tmp += "Max allowed sequence size is: "+str(maxSeqSize)+"."
        # write error message to error file
        err.write(tmp)
    # close the error file
    err.close()