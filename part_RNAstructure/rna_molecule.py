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
                print "Error while trying to find the parsed database..."
                return False
                #self._err.write("-------Error in mod RNA_molecule: \n",
                #                "Issue with the path to the database. File "\
                #                "or directory does not exists.",\
                #                "\n-------------------")
        else:
            return True


def parse_database(path_db):
    db_name = "rna.struc"
    path_db += db_name
    print path_db

    handler = open(path_db, "w")
    print "Worked..."
    return handler


def main():
    mol = RNA_molecule("CATGC", "HI-V", "test")
    mol.print_rna_information()
    mol.db_parsed("RNA_STRAND_data/")
    mol.print_rna_information()

main()
