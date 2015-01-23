#####################################################################

# Edgar Olijar
# sequence_import.py

import re
import ntpath
import datetime
from Bio import SeqIO
from Bio import Entrez
from urllib2 import HTTPError
import os

#####################################################################

def addtext(label, txt):
    # Add status to label
    currentLabelText = label['text']
    currentLabelText += txt + '\n'
    # Writing it on the label
    label.config(text = currentLabelText)

#####################################################################

# GET SEQUENCE FROM DATABASE (NCBI)

# Get sequence from NCBI's Entrez databases
# Output of this function is of class:
# <class 'Bio.SeqRecord.SeqRecord'>
# 'geneID' must contain only 1 gene ID
# input type: integer.
# 'err' is an error file
def inputFromDB(geneID,err,userEmail,label):
    # get current time:
    timeStamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    geneID = str(geneID)
    # check if gene ID is empty:
    if(geneID == ""):
        tmp = "Error in function 'inputFromDB'. No gene ID found."
        err.write(tmp)
    # check if there are multiple gene ID's
    # if yes, then they would be delimited 
    # by comma. multiple ID's are not allowed
    gene_ids_arr = str.split(geneID, ",")
    if(len(gene_ids_arr) > 1):
        tmp = "Error in function 'inputFromDB'. "
        tmp += "Multiple gene ID's detected. "
        tmp += "Multiple gene ID's are separated by comma."
        err.write(tmp)
    ### addtext(label, "Gene ID successfully checked!")
    Entrez.email = userEmail
    # try to download the sequence from database
    try:
        # Entrez.efetch will return an XML file. you can also use
        # instead of "retmode='text'" the parameter "retmode='fasta'"
        handle = Entrez.efetch(db="nuccore",id=geneID,rettype="gb",retmode="text")
        # more informations about functions and parameters:
        # http://biopython.org/DIST/docs/api/Bio.Entrez-module.html
        # http://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
    except HTTPError, e:
        tmp = timeStamp+". Error in function 'inputFromDB'. "
        tmp += str(e)
        tmp += ". It seems that there is no data available under this gene ID."
        # write error message to error file
        err.write(tmp)
        return -1
    txt = "Requested data was successfully downloaded from NCBI server."
    ### addtext(label, txt)
    # get sequence (class 'Bio.SeqRecord.SeqRecord')
    try:
        SeqRecord = SeqIO.read(handle, "genbank")
    except ValueError, e:
        tmp = timeStamp+". Error in function 'inputFromDB'. "+str(e)
        # write error message to error file
        handle.close()
        err.write(tmp)
    handle.close()
    return SeqRecord

#####################################################################

# GET SEQUENCE FROM FILE

# Get path to fasta file and return a sequence.
# Output of this function is of class:
# <class 'Bio.SeqRecord.SeqRecord'>
# The input file must contain only 1 sequence.
# 'err' is an error file
def inputFromFile(filePath,err,label):
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
    # check if input file is empty
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
        txt = "All data was successfully extracted from input file."
        addtext(label, txt)
        return SeqRecord
    # is it a RNA ?
    if(bool(re.match("^[ACGU]+$", sequence))):
        txt = "All data was successfully extracted from input file."
        addtext(label, txt)
        return SeqRecord
    else:
        tmp = timeStamp + ". "
        tmp += "Error in function 'inputFromFile'. "
        tmp += "Sequence contains wrong characters."
        # write error message to error file
        err.write(tmp)

#####################################################################

# CONVERTER:
# <class 'Bio.SeqRecord.SeqRecord'> TO FastA file

# *** input: 
# - filePath      = path to fasta file
# - Seq_Record    = object of class '<class 'Bio.SeqRecord.SeqRecord'>'
# - err           = error file
# *** output:
# - fasta file
# function returns nothing, but the side effect of the 
# function is that it produces a FASTA file
def seqRecord2fasta(filePath,Seq_Record,err,label):
    # get current time
    timeStamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    # Check if file was chosen
    if(filePath == None):
        tmp = timeStamp + ". "
        tmp += "Error in function 'seqRecord2fasta'. Empty file path."
        # write error message to error file
        err.write(tmp)
    # get file name and file extension. 
    # I use here module 'ntpath' to get file name, 
    # because it is more system independent than module 'os'.
    fileName, fileExtension = ntpath.splitext(filePath)
    if(fileName == ""):
        tmp = timeStamp + ". "
        tmp += "Error in function 'seqRecord2fasta'. No file was chosen."
        # write error message to error file
        err.write(tmp)
    # check if 'fileName' has the correct extension.
    # Allowed are: '.txt', '.fa', '.fasta'
    fileExtensions = ['.txt', '.fa', '.fasta']
    if(fileExtension not in fileExtensions):
        tmp = timeStamp + ". "
        tmp += "Error in function 'seqRecord2fasta'. Wrong file selected. "
        tmp += "Allowed file extensions are: '.txt', '.fa', '.fasta'."
        # write error message to error file
        err.write(tmp)
    # try to open the file
    try:
        output_handle = open(filePath, "w")
    except ValueError, e:
        tmp = timeStamp + ". "
        tmp += "Error in function 'seqRecord2fasta'. " + str(e)
        # write error message to error file
        err.write(tmp)
    SeqIO.write(Seq_Record, output_handle, "fasta")
    output_handle.close()
    txt = "Fasta file was successfully created."
    addtext(label, txt)

#####################################################################

# input: object of type '<class 'Bio.SeqRecord.SeqRecord'>'
# output: string (sequence)
def get_sequence_from_SeqRecord(seq_record):
    return seq_record.seq

# CHECK SEQUENCE SIZE

# check size of the sequence
# maxSeqSize = max allowed size of the sequence
def checkSeqSize(seq,maxSeqSize,err,label):
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
    txt = "Sequence was successfully checked. All checks passed."
    addtext(label, txt)
