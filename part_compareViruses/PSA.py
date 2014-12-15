__author__ = "Mirjam Figaschewski"

'''
This package implements pairwise sequence alignment using a dynamic
programming algorithm.

This provides functions to get global and local alignments between two
sequences.  A global alignment finds the best concordance between all
characters in two sequences.  A local alignment finds just the
subsequences that align the best.

One needs:
seq1, seq2          strings
RNA, DNA            boolean:what shall be aligned?
                    (default: True, False)

following parameters are also need to be set for local alignment (_local):
align_global        boolean: shall a global alignment be performed?
                    (default: True)
match_global        tupel (int, int): match score and mismatch score
                    (default: (1, 0))
samePenalties_global boolean: use same gap panelties for both sequences?
                    (default = True)
same_gap_global     tupel (int, int): gap open panelty, extension panelty
                    (default: (0, 0))
differentPenalties_global: coolean: use different gap panelties for sequences?
                    (default: False)
gap_diff_global: tupel(int, int, int ,int): gap open seq1, extension seq 1,
                    gap open seq2, extension seq2
                    (default: (-.5, -.1, -.6, -.4))
'''

import os
import sys
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from collections import Counter


def localAlign(
        seq1, seq2, match_local, samePenalties_local, same_gap_local,
        differentPenalties_local, gap_diff_local):
    match_score = match_local
    if samePenalties_local:
        print "Local Alignment with same gap panelties"
        for a in pairwise2.align.localms(
                seq1, seq2,
                match_score[0], match_score[1],
                same_gap_local[0], same_gap_local[1]):
            print format_alignment(*a)
    elif differentPenalties_local:
        print "Local Alignment with different gap panelties"
        for a in pairwise2.align.localmd(
                seq1, seq2,
                match_score[0], match_score[1],
                gap_diff_local[0], gap_diff_local[1],
                gap_diff_local[2], gap_diff_local[3]):
            print format_alignment(*a)


def globalAlign(
        seq1, seq2, match_global, samePenalties_global, same_gap_global,
        differentPenalties_global, gap_diff_global):
    match_score = match_global
    if samePenalties_global:
        print "Global Alignment with same gap panelties"
        for a in pairwise2.align.globalms(
                seq1, seq2,
                match_score[0], match_score[1],
                same_gap_global[0], same_gap_global[1]):
            print format_alignment(*a)
    elif differentPenalties_global:
        print "Global Alignment with different gap panelties"
        for a in pairwise2.align.globalmd(
                seq1, seq2,
                match_score[0], match_score[1],
                gap_diff_global[0], gap_diff_global[1],
                gap_diff_global[2], gap_diff_global[3]):
            print format_alignment(*a)


def alignSequences(
        seq1, seq2, RNA=True, DNA=False,
        align_global=True, match_global=(1, 0), samePenalties_global=True,
        same_gap_global=(0, 0), differentPenalties_global=False,
        gap_diff_global=(-.5, -.1, -.6, -.4),
        align_local=True, match_local=(1, 0), samePenalties_local=True,
        same_gap_local=(0, 0), differentPenalties_local=False,
        gap_diff_local=(-.5, -.1, -.6, -.4)):
    if (RNA and DNA):
        print("Error in aligning two sequences:\n\
            Need to choose one type of sequences: \n\
            both RNA OR both DNA OR both Proteins")
        return
    dna_bases = ("A", "G", "C", "T")
    rna_bases = ("A", "G", "C", "U")
    count1 = Counter(seq1)
    count2 = Counter(seq2)
    dna_seq1 = all(base in dna_bases for base in count1)
    rna_seq1 = all(base in rna_bases for base in count1)
    dna_seq2 = all(base in dna_bases for base in count2)
    rna_seq2 = all(base in rna_bases for base in count2)

    if DNA:
        if(not dna_seq1 or not dna_seq2):
            print("Error in aligning two sequences:\n\
                    Given sequences are not both DNA sequences:")
            print"Sequence1 is a DNA sequence?", dna_seq1
            print"Sequence2 is a DNA sequence?", dna_seq2
            return
    if RNA:
        if(not rna_seq1 or not rna_seq2):
            print("Error in aligning two sequences:\n\
                    Given sequences are not both RNA sequences:")
            print"Sequence1 is a RNA sequence?", rna_seq1
            print"Sequence2 is a RNA sequence?", rna_seq2
            return
    if align_global:
        globalAlign(
            seq1, seq2, match_global,
            samePenalties_global, same_gap_global, differentPenalties_global,
            gap_diff_global)
    if align_local:
        localAlign(
            seq1, seq2, match_local,
            samePenalties_local, same_gap_local, differentPenalties_local,
            gap_diff_local)


if __name__ == "__main__":
    seq1 = "ACCGT"
    seq2 = "ACT"
    alignSequences(seq1, seq2, DNA=True, RNA=False)
    seq3 = "AGUC"
    seq4 = "AGCUA"
    alignSequences(seq3, seq4, RNA=True, DNA=False)
