import sys
import os
import predictORFs as p

__author__ = 'Felix Bartusch'


# Transcribe a given DNA sequence to the corresponding RNA sequence.
def transcribe(seq):
    dna2rna = {"A": "U", "T": "A", "C": "G", "G": "C"}
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
def getCodonTable():
    bases = ['U', 'C', 'A', 'G']
    codons = [a + b + c for a in bases for b in bases for c in bases]
    aa = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
    return dict(zip(codons, aa))


# Translate a given RNA sequence to the corresponding protein.
def translate(seq):
    # The growing protein
    protein = ""
    # Translate each codon to the corresponding amino acid
    for x in range(0, len(seq), 3):
        codon = seq[x:x + 3]
        codon_table = getCodonTable()
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
        w.write("TranslateToProtein:")
        w.write("\tThere are no ORFs to translate!")
    print "Start translating ORFs to proteins"
    for orf in orfs:
        # TODO is it correct to just replace "T" with "U"?
        # I think at least for HIV-1 it is correct
        orf["sequence"] = translate(dnaAsRNA(orf["sequence"]))
    print "Translated", len(orfs), "ORFs to proteins"
    print "End translating ORFs to proteins!"
    # The sequence of the orfs is now the protein sequence,
    # so we're done here!
    return orfs


# Test!
def main():
    # Error log
    r, err = os.pipe()
    err = os.fdopen(err, 'w')
    # Predict ORFs
    path = sys.argv[1]
    # Read the input file
    headers, seqs = p.readFasta(path, err)
    # We have just one sequence
    seq = seqs[0]
    # Predict the ORFs
    orfs = p.predictORFS(seq, err)
    # Translate the ORFs into the protein sequence
    proteins = translateToProtein(orfs, err)
    # How Print the resulting list of proteins
    for protein in proteins:
        print protein
    print "Translated", len(proteins), "proteins."


if __name__ == "__main__":
    main()