#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# ViralToolBox
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Skript predictORFS.py
# Skript translateToProtein.py
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 			@authors: Felix Bartusch
#
###############################################################

You need to import the two scripts:
	a) predictORFS.py
	b) translateToProtein.py

No other python packages are used in that scripts!

Description of important functions:

### function: predictORFS(seq, w):
-----------------------------------------------------
Creates a list of ORFs of the DNA sequence seq. The list of ORFs consists of
dictionaries describing the ORFs. Keys of the dictionary are:
'start' : 	The position of the first nucleotide of the ORF in the sequence
'end':			The position of the last nucleotide of the ORF in the sequence
'sequence'	The nucleotide sequence of the ORF


### function: translateToProtein(orfs, w):
-----------------------------------------------------
The object orfs is a list describing orfs in a DNA sequence. You can take the object returned
by predictORFS as input for translateToProtein.
The only thing this function does is to translate the DNA sequence to the corresponding
amino acid sequence. It returns a list containing a dictionary describing the proteins with
the following keys:

'start' : 	The position of the first nucleotide of the protein in the sequence
'end':			The position of the last nucleotide of the protein in the sequence
'sequence'	The protein sequence of the protein coded in the region [start, end] of the sequence.

### function main() in the file translateToProtein.py
-----------------------------------------------------
This tests both the ORF prediction and the following translation to the protein sequence.
This can be tested by calling the script from the command line
providing the path to a fasta file containing the sequence of the virus.
The predicted and translated proteins will then be printed to command line.


All other functions are just helper functions called by predictORFs.

