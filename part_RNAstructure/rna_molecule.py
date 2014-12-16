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
import os
from time import gmtime, strftime


class RNA_molecule:
    def __init__(self, sequence, name, err):
        self._sequence = sequence
        self._name = name
        self._err = err
        self._structure = None
        self._database = None

    def print_rna_information(self):
        print "\n--------RNA molecule information"
        print "Sequence: \t", len(self._sequence), "bp"
        print "Name: \t\t", self._name
        print "Database: \t", self._database
        if self._structure is None:
            print "Structure: \tNot searched in database yet."\
                  "No prediction done so far."
        else:
            print "Structure: \n", self._structure
        print "--------end information\n"

    def db_parsed(self, path_db):
        if self._database is None:
            try:
                print "Searching for <struc> database..."
                for file in os.listdir(path_db):
                    if file.endswith(".struc"):
                        print "Found db: ", file
                        self._database = file
                        return True
                print "No parsed database found so far."
                print "..Building <struc> database from ct-files in:",\
                      path_db
                self._database = parse_database(path_db)
                return True
            except OSError:
                print "-------Error in mod RNA_molecule: \n",\
                      strftime("%a, %d %b %Y %H:%M:%S", gmtime()), "\n",\
                      "Issue with the path to the database. File "\
                      "or directory does not exists.",\
                      "\n-------------------------------"
                return False
                #self._err.write("-------Error in mod RNA_molecule: \n",
                #                "strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())\n",
                #                "Issue with the path to the database. File "\
                #                "or directory does not exists.",\
                #                "\n-------------------")
        else:
            return True


def parse_database(path_db):
    db_name = "rna.struc"
    path_db_file = path_db + db_name
    print path_db_file

    handler = open(path_db_file, "w")

    # read all ct-file in the directory of the database path
    for file in os.listdir(path_db):
        # check if file is a ct-file
        if file.endswith(".ct"):
            ct_file = open(path_db+file, "r")
            seq_length = 0
            newick_str = None
            sequence_str = None
            # go through every line of the file
            for line in ct_file:
                # skip the comment lines
                if line[0] is not "#":
                    print file
                    print line
                    print seq_length
                    if seq_length is 0:
                        # get the sequence length number
                        seq_length = int(filter(None, (line.split(" ")))[0])
                        newick_str = [None] * seq_length
                    else:
                        # make list from to extract the bracket and dots
                        # positions
                        line = filter(None, line.split(" "))
                        if newick_str[int(line[2])] is None:
                            # when a dot notation should be done
                            if int(line[4]) is 0:
                                newick_str[int(line[2])] = "."
                            else:
                                # make the opening and closing brackets
                                newick_str[int(line[2])] = "("
                                newick_str[int(line[4])] = ")"
        print "".join(newick_str)
    return path_db_file


if __name__ == "__main__":
    mol = RNA_molecule("CATGC", "HI-V", "test")
    mol.print_rna_information()
    mol.db_parsed("RNA_STRAND_data/")
    mol.print_rna_information()
