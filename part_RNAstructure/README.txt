#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# ViralToolBox
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Module <rnaStruc>
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 			@authors: Simon Heumos, Sven Fillinger
#
###############################################################

You need all three python files:
	a) rna_molecule.py
	b) db_entry.py
	c) RNASecStructPrediction.py

You need the ViennaRNA package with rna_fold!!
	Download ---> http://www.tbi.univie.ac.at/RNA/index.html#download



!!! Important objects:
....<struc> database
A struc database stores the entries in lines, each line 
contains the hash-code of the sequence, the sequence itself and the 
Newickstring as structural information (all tab delimeted).
	<hash-value seq>    <sequence>      <newick_str>

...RNA_molecule
A RNA_molecule object contains the sequence, the path to the <struc> database
and the structural information.
At initialization, only Sequence and Name are stored in the object, as well
as the output pipeline. With certain function explained further down this page, 
this Object can be extended with information such as Database-path and structure.

...DB_entry
Normally entries of the <struc> database are read in as DB_entry objects.
They contain information such as the hash-code, the sequence and the newickstring.
Certain getter methods are provided to call this variables.



Description:

### function: RNA_molecule(sequence, name, pipeline)
-----------------------------------------------------
Create a RNA_molecule object with a sequence, a name, and an output
pipeline (i.e. err in our project casse). Normal outputs will be 
called with the normal "print" function (sys.stdout).


### <RNA_molecule>.parsed(path)
-------------------------------
Let's say you have several ct-files downloaded with structural information
of RNA molecules. Give the path and run this function, and it will create
a <struc> database from them. If in the given path, a <struc> database already
exists, then this function will choose this db automatically.
The final path to the db will be stored in the RNA_molecule object.


### <RNA_molecule>.print_rna_information()
------------------------------------------
Prints the current RNA_molecule information.


### parse_struc_db(struc_db)
----------------------------
Returns a dictionary containing the information of the <struc> database.
KEY: hash-code of sequence  VALUE: DB_entry object


### <RNA_molecule>.search_rna_structure(struc_db)
------------------------------------------------
Expects an DICTIONARY like the one described above, if an entry for the molecule is there it stores
the structural information in the RNA_molecule object.
If not in the database, then automatically the ZUCKER-algorithm will be performed
on the sequence of the RNA_molecule object and the result stored in the object again.



### <RNA_molecule>.get_sequence()
### <RNA_molecule>.get_structure()
### <RNA_molecule>.get_database()
### <RNA_molecule>.get_name()
### <RNA_molecule>.get_energy()


