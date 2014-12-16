#! /usr/bin/python2.7

import sys
import os
from Bio.Seq import Seq
from Bio import SeqIO
import subprocess 


# runs RNAfold and returns the output 
def runRNAfold(RNA):
	cmd = ['echo']
	cmd.append(RNA)	
	p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	p2 = subprocess.Popen(['RNAfold'],stdin=p1.stdout,stdout=subprocess.PIPE)
	p1.stdout.close()
	output = p2.stdout.read() 
	return str(output)


# takes the output of an RNAfold or RNAcofold and returns the secondary structure
def get_sec_struc(output):
	out_split = output.split()
	return out_split[1]


# parses the output of RNAfold and RNAcofold and returns the energy score
def get_score(output):
	out_split = output.split("\n")[1].split(" ")[2]
	out_split = out_split[:-1]
	energy = 0.0
	try:
		energy = float(out_split)
	except ValueError ,e:
		print "Error: ",e
		print output
	return energy
	

################### -- main -- ###################
def main():
	print "test"
	rna = "ACACGACGUAGCGUUAGACGUGACGUAGACGUAGAC"
	output = runRNAfold(rna)
	print output
	print get_sec_struc(output)
	print get_score(output)


if  __name__ =='__main__':
	# check number of input arguments and print help
	#if len(sys.argv) != 3: 
	#	print "RNACofolding.py takes two multiple fasta-files and computes the folding and the cofolding of all pairs of RNAs. "
	#	print "It returns tab-separated tables of these combinations with the following elements: "
	#	print "E(x) is the energy score of the ViennaRNA folding / cofolding algorithm (normalized by length of input) "
	#	print "LD(x) is the energy score of the Loop Decomposition algorithm (normalized by length of input) "
	#	print "log_p_value(x) is the log-p-value that the score occurs by chance"
	#	print
	#	print "How to run this program: "
	#	print "RNACofolding.py <first multiple fasta-file> <second multiple fasta-file>"

	#else:
	#	main(sys.argv[1],sys.argv[2])
	main()