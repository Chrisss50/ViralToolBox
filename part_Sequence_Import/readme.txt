Additional notes to the script "sequence_import.py"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

project: ViralToolBox
lecture: Bioinformatics 1, 2014/2015
project part: part_Sequence_Import
author: Edgar Olijar

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python packages used by this script and has to be installed:

re
ntpath
datetime
Bio

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are 5 functions in the script:

1) inputFromDB(geneID,err,email)
2) inputFromFile(filePath,err)
3) seqRecord2fasta(filePath,Seq_Record,err)
4) get_sequence_from_SeqRecord(seq_record)
5) checkSeqSize(seq,maxSeqSize,err)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1) 
*** inputFromDB : parameters
- geneID : gene ID, can be string or integer
- err    : error file
- email  : user email (string)
*** output
the function returns an object of class:
<class 'Bio.SeqRecord.SeqRecord'>

2) 
*** inputFromFile : parameters
- filePath : path to txt/fasta/fa file
- err      : error file
*** output
the function returns an object of class:
<class 'Bio.SeqRecord.SeqRecord'>

3)
*** seqRecord2fasta : parameters
- filePath      : file path to txt/fasta/fa file
- Seq_Record    : object of class <class 'Bio.SeqRecord.SeqRecord'>
- err           : error file
*** output:
- function has no output, but has a side effect:
  if no errors occurred, then it produces a FASTA file

4)
*** get_sequence_from_SeqRecord : parameters
- seq_record : object of class <class 'Bio.SeqRecord.SeqRecord'>
*** output
- string (sequence)

5)
*** checkSeqSize : parameters
- seq         : sequence (string !)
- maxSeqSize  : MAX allowed length of the sequence (specified by user)
- err         : error file
*** output
there is no output, the function can only return some error messages

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

How to invoke ?
IF you have a txt/fasta/fa file
   USE: inputFromFile
IF you want to get file from data base (NCBI)
   USE: inputFromDB
   
once you have downloaded/read in the file,you can check
the size of the sequence with function: 'checkSeqSize'.
This function needs as input a string, but functions 
'inputFromFile' and 'inputFromDB' return objects of class
'<class 'Bio.SeqRecord.SeqRecord'>', so we need to get the 
sequence. Here we can use the function 'get_sequence_from_SeqRecord'
which receives an object of class '<class 'Bio.SeqRecord.SeqRecord'>'
and returns a string (sequence).

IF you want to convert the object of class 
   '<class 'Bio.SeqRecord.SeqRecord'>' to FASTA file (.fa/.fasta/.txt), then:
   USE: seqRecord2fasta

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~