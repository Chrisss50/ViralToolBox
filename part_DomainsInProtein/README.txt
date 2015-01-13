#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# ViralToolBox
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Part domainsInProtein
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 			@authors: Felix Bartusch
#
###############################################################

You need to import the scripts:
	a)  domainsInProtein.py

Python packages used by this script and has to be installed:
pycurl
urllib
urllib2
time
json
pickle
StringIO import StringIO
selenium import webdriver
pyvirtualdisplay import Display
PIL import Image

!!!!!! ALSO THE FIREFOX BROWSER HAS TO BE INSTALLED !!!!
The script runs javascript code in a browser and extracts a graphical output not coded in the xml code,
so this is the only way I know getting nice pictures of the domains.

	

Description of important functions:

### findDomains(proteins, baseDir, err):
-----------------------------------------------------
This function finds domains in the proteins and generates pictures visualizing the domains.
The first parameter is a list of proteins. Each protein is discribed by a dictionary containing the
following keys:
'start' : 	The position of the first nucleotide of the protein in the sequence
'end':			The position of the last nucleotide of the protein in the sequence
'sequence'	The protein sequence of the protein coded in the region [start, end] of the sequence.

To fulfill the desired task, pfam (http://pfam.xfam.org/search) is queries for each protein. The URLs directing to the
results is saved and a few seconds later the result is obtained from pfam.
The resulting domains are then visualized by pfam. The visualization is extracted from that website, that runs in the firefox
browser opened by the python script.

The output of the translateToProtein function in the file translateToProtein.py can be used as input for this function.
The function itself returns, beside the output written to the baseDir, a list describing the domains in the given proteins.
To do so, several keys were added to the dictionary:
'domains':						A json string describing the domains of a protein. Can be used by pfam to generate a visualization of the domains
'domain_graphic_path'	Path to the graphic describing the domain of a protein
'result_url'					URL with the result of the pfam sequence search query
'job_id'							ID given by pfam for that job

The pictures of the domaisn are saved in the directory given as second parameter to the function.
Also a result file names result.txt is written in the baseDir, summarising important properties of each domain in the proteins.

### function main() in the file domainsInProtein.py
-----------------------------------------------------
This tests the findDomains method. A example protein is used and the output is written in the
current working directory.

All other functions are just helper functions called by predictORFs.

