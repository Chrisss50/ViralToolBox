Additional notes to the script "sequence_import.py"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are 4 functions in the script:
1) inputFromDB(geneID,err,email)
2) inputFromFile(filePath,err)
3) get_sequence_from_SeqRecord(seq_record)
4) checkSeqSize(seq,maxSeqSize,err)

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
*** get_sequence_from_SeqRecord : parameters
- seq_record : object of class <class 'Bio.SeqRecord.SeqRecord'>
*** output
- string (sequence)

4)
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

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~