import sys
import os
import predictORFs as p

__author__ = 'Felix Bartusch'


# Transcribe a given DNA sequence to the corresponding RNA sequence.
dna2rna = {"A": "U", "T": "A", "C": "G", "G": "C"}
def transcribe(seq):
    transcript = ""
    for c in seq:
        transcript += dna2rna[c]
    return transcript


# Just replauce T with U
def dnaAsRNA(seq):
    return seq.replace("T", "U")


# Generate the mapping from codons to amino acids
# from:
# http://www.petercollingridge.co.uk/python-bioinformatics-tools/codon-table
# because this is easier than writing all the codons with my hands ;)
bases = ['U', 'C', 'A', 'G']
codons = [a + b + c for a in bases for b in bases for c in bases]
aa = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
codon_table = dict(zip(codons, aa))


# Translate a given RNA sequence to the corresponding protein.
def translate(seq):
    # The growing protein
    protein = ""
    # Translate each codon to the corresponding amino acid
    for x in range(0, len(seq), 3):
        codon = seq[x:x + 3]
        aa = codon_table[codon]
        if aa != "*":
            protein += aa
        else:
            # We found the stop codon
            break
    return protein


# Transcribe and Translate all ORFs to their amino acid sequence
def translateToProtein(orfs, w):
    # Handling errors
    if orfs is None or len(orfs) == 0:
        w.write("________________")
        w.write("Error-Log of translateToProtein:")
        w.write("There are no ORFs to translate!")
    print "Start translating ORFs to proteins"
    for orf in orfs:
        # TODO is it correct to just replace "T" with "U"?
        # I think at least for HIV-1 it is correct accord
        orf["sequence"] = translate(dnaAsRNA(orf["sequence"]))
    print "Translated", len(orfs), "ORFs to proteins"
    print "End translating ORFs to proteins!"
    # The sequence of the orfs is now the protein sequence,
    # so we're done here!
    return orfs

if __name__ == "__main__":
    # path to the fasta input file
    path = sys.argv[1]
    # Read the input file
    headers, seqs = p.readFasta(path)
    # We have just one sequence
    seq = seqs[0]
    # Predict the ORFs
    w = os.pipe()
    orfs = p.predictORFS(seq, w)
    
    proteins = translateToProtein(orfs, w)
    # How many ORFs have we found?
    # Print the ORFs
    for protein in proteins:
        print protein