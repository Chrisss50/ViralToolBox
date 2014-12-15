# :::::::: # :::::::: # :::::::: # :::::::: # :::::::: #
#
# Viral Tool Box
# ------------------
# module RNA secondary structure prediction
#
# Features:
#   * Class rna_molocule
#   * contains the sequence and the virus name
#   * calls the database for possible matches
#   * calls structure prediction tools
#   * visualizes the secondary structure (png, jpg or svg)
#   (* compares structures)
#
#
#              @authors: Simon Heumos and Sven Fillinger
# :::::::: # :::::::: # :::::::: # :::::::: # :::::::: #


class RNA_molecule:
    def __init__(self, sequence, name, err):
        self._sequence = sequence
        self._name = name
        self._err = err

    def print_sequence(self):
        print self._sequence


def main():
    mol = RNA_molecule("CATGC", "HI-V", "test")
    mol.print_sequence()

main()
