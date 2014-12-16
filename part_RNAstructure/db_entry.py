# :::::::: # :::::::: # :::::::: # :::::::: # :::::::: #
#
# Viral Tool Box
# ------------------
# module RNA secondary structure prediction
#
# Features:
#   * Class db_entry
#   * hash_code of the sequence
#   * sequence
#   * newick
#
#
#              @authors: Simon Heumos and Sven Fillinger
# :::::::: # :::::::: # :::::::: # :::::::: # :::::::: #


class DB_entry:
    def __init__(self, hash_code, sequence, newick_str):
        self._hash_code = hash_code
        self._sequence = sequence
        self._newick_str = newick_str

    def get_hash(self):
        return self._hash_code

    def get_sequence(self):
        return self._sequence

    def get_newick_str(self):
        return self._newick_str

    def part_of_sequence(self, sequence):
        return sequence in self._sequence


if __name__ == "__main__":
    test_object = DB_entry("6dggd27727gd",
                           "CTAGCTATTTATATAT",
                           ".....((())))...")
    print test_object.part_of_sequence("CTATT")
    print test_object.part_of_sequence("GGT")
