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
import hashlib
import shutil
from db_entry import DB_entry
from time import gmtime, strftime
import RnaSecStructPrediction as prediction


class RNA_molecule:
    '''The RNA_molecule class.
       Contains information about:
            * the sequence
            * the name
            * the error pipe for err logging
            * the structure in newick format
            * the path to the <struc> database'''
    def __init__(self, sequence, name, err):
        self._sequence = sequence
        self._name = name
        # the error pipe
        self._err = err
        self._structure = "not determined yet" 
        self._database = "no database found yet"
        self._energy = 0
        print "Object RNA_molecule created."
        print self.print_rna_information()

    def get_sequence(self):
        return self._sequence

    def get_structure(self):
        return self._structure

    def get_database(self):
        return self._database

    def get_name(self):
        return self._name

    def get_energy(self):
        return self._energy

    def print_rna_information(self):
        '''Prints the information stored in the RNA molecule
           object. (Sequence, structure, name, database, etc)'''

        print "\n--------RNA molecule information"
        print "Sequence: \t", len(self._sequence), "bp"
        print "Name: \t\t", self._name
        print "Database: \t", self._database
        if self._structure is None:
            print "Structure: \tNot searched in database yet."\
                  " No prediction done so far."
        else:
            print "Energy: \t", self._energy
            print "Structure: \n", self._sequence + "\n" + self._structure
        print "--------end information\n"

    def db_parsed(self, path_db):
        '''This function searches in the given path (has to be a directory)
           for an <struc> database. 
           If one is there, assign it to the RNA_molecule, if not, create
           a <struc> database out of all ct-files.
           !! NOTE: the path has also to contain the ct-files, otherwise
           you cannot construct a <struc> database'''

        if self._database is None:
            try:
                print "Searching for <struc> database..."
                for file in os.listdir(path_db):
                    if file.endswith(".struc"):
                        print "Found db: ", file
                        self._database = path_db + file
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

    def search_rna_struc(self, dict_db, path):
        '''Given a directory with hash values of sequences
           as <keys> and DB_entry objects as <values>,
           this function searches the given sequence of the
           rna_molecule object in the directory.
           If no entry is found, then automatically predict
           the structure with the Zucker algorithm'''

        hash_object = hashlib.sha256(self._sequence)
        try:
            db_entry = dict_db[hash_object.hexdigest()]
            print "Found structure in database!"
            self._structure = db_entry.get_newick_str()
            print "Dot bracket format:\n", self._structure
            prediction.runRNAplot(self._name, self._sequence, self._structure)
            os.remove(self._name + ".ps")
            shutil.move(self._name + "_ss.ps", path + "/sec_struct" + ".ps")
        except:
            # Do the structure prediction if the structure is not
            # in the database
            print "Structure not found in database!"
            print "Trying secondary structure prediction using RNAfold...."
            ####implement simons stuff
            try:
                structure_pred = prediction.runRNAfold(self._sequence)
                self._structure = prediction.get_sec_struc(structure_pred)
                self._energy = prediction.get_score(structure_pred)
                shutil.move("rna.ps", path + "/sec_struct" + ".ps")
                print "Structure predicted sucessfully."
            except:
                print "Error, something went wrong with the structure "\
                        "prediction!"
        return True


    def writeTXT(self, path):
	file = path + "/sec_struct.txt"
        handler = open(file, "w")
        n = "\n"
        t = "\t"
        handler.write("NAME:" + n + self._name + n + "SEQUENCE:" + n + self._sequence + n + "STRUCTURE:" + n + self._structure + n + "ENERGY:" + n + str(self._energy))


def parse_struc_db(path_db):
    '''Creates a dictionary out of a <struc> database
       Key will be the hash-code of the sequence and value
       will be a DB_entgry object'''

    dic_structures = {}
    try:
        struc_file = open(path_db)
        for line in struc_file:
            line = line.split()
            dic_structures[line[0]] = DB_entry(line[0], line[1], line[2])
    except:
        print "Could not open file: ", path_db
    return dic_structures


def parse_database(path_db):
    ''' Pasrsing of all the ct-files and creates the <struc>
        database. The database will contain lines with following format:
            <hash-value seq>    <sequence>      <newick_str>'''

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
            sequence_str = ""
            # go through every line of the file
            for line in ct_file:
                # skip the comment lines
                if line[0] is not "#":
                    if seq_length is 0:
                        # get the sequence length number
                        seq_length = int(filter(None, (line.split()))[0])
                        newick_str = [None] * seq_length
                    else:
                        # make list from to extract the bracket and dots
                        # positions
                        line = filter(None, line.split())
                        sequence_str += line[1]
                        try:
                            if newick_str[int(line[2])] is None:
                                # when a dot notation should be done
                                if int(line[4]) is 0:
                                    newick_str[int(line[2])] = "."
                                else:
                                    # make the opening and closing brackets
                                    newick_str[int(line[2])] = "("
                                    newick_str[int(line[4])-1] = ")"
                        except:
                            print "Corrupt file: ", file
                            """self._err.write("-------Error in mod RNA_molecule: \n",\
                                            strftime("%a, %d %b %Y %H:%M:%S", gmtime()), "\n",\
                                            "Corrupt file: ", file,\
                                            "\n-------------------------------")"""
                            break
            try:
                newick_str = "".join(newick_str)
                hash_object = hashlib.sha256(sequence_str)
                print_str = (hash_object.hexdigest() + "\t" +
                             sequence_str + "\t" + newick_str + "\n")
                handler.write(print_str)
            except:
                print "Corrupt file: ", file
        #except:
        #    print "ohoooo"
    handler.close()
    print "<struc> database build successfully"
    return path_db_file


if __name__ == "__main__":
    """ You can test the functions here."""
    # create a RNA_molecule object
    mol = RNA_molecule("ACACGACGUAGCGUUAGACGUGACGUAGACGUAGAC", "HI-V", "test")
    # search for the <struc> database in a directory
    # if not there, from the ct-files a <struc>database is
    # created
    mol.db_parsed("RNA_STRAND_data/")
    # Print the information of your current RNA object
    #    * Structure
    #    * Name
    #    * Database path
    #    * Sequence
    mol.print_rna_information()
    # parse the <struc> database and create a dictionary with
    # the hash values of the sequence as <keys> and DB_entry
    # objects as <value>
    struc_db = parse_struc_db(mol.get_database())
    # once you have a dictionary with all the database entries
    # you can call the search_rna_struc() function from your
    # rna_molecule object
    mol.search_rna_struc(struc_db, "./")
    mol.print_rna_information()
    mol.writeTXT("./")
