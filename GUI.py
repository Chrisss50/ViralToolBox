import tkFileDialog
from Tkinter import *
sys.path.append("part_PredictAndTranslateORFs/")
from predictORFs import *
from translateToProtein import *
sys.path.append("part_DomainsInProtein/")
import domainsInProtein as d
sys.path.append("part_Sequence_Import/")
from sequence_import import *
sys.path.append("part_RNAstructure/")
from RnaSecStructPrediction import *
from rna_molecule import *
sys.path.append("part_PdfReport/")
from write_comparePdf import *
from writePdf import *
sys.path.append("part_compareViruses/")
from compareViruses import *
sys.path.append("part_msa/")
from msa_functions import *
sys.path.append("part_phylogeny/")
from phyl_functions import *

class App:
  # Global variables used for saving needed dialogs
  txt = ""
  fileDir = " "
  dbDir = " "
  logo = ""

  # Building the UI
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
    frameLeft = Frame(frame)
    frameLeft.pack(side=LEFT)
    frameRight = Frame(frame)
    frameRight.pack(side=RIGHT)
    self.logo = PhotoImage(file="Logo.gif")

    # Right-Frame (Status-Box)
    self.label = Label(frameRight, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       bg="light grey",
                       height=38,
                       width=100)
    self.label.pack(side = BOTTOM)
    self.labelLogo = Label(frameRight,
                       bg="white",
                       image = self.logo)
    self.labelLogo.pack()

    # Left-Frame (Buttons)
    # Pipeline
    self.labelpipeStart = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=7)
    self.labelpipeStart.pack()
    self.labelpipeStart.config(text = "Pipeline:", font="Verdana 15 bold")
    self.labelVName = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=10)
    self.labelVName.pack()
    self.labelVName.config(text = "Identifier:")
    self.textVName = Text(frameLeft,
                     bg="light blue",
                     height=1,
                     width=20)
    self.textVName.pack()
    self.textVName.insert(END, "Banana Virus")
    self.labelInput = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=10)
    self.labelInput.pack()
    self.labelInput.config(text = "Result Path:")
    self.getDirIn = Button(frameLeft, 
                         text="Get directory", fg="red",
                         command=self.getDirectory)
    self.getDirIn.pack()
    self.text1 = Text(frameLeft,
                     bg="light blue",
                     height=1,
                     width=20)
    self.text1.pack()
    self.text1.insert(END, "GUI_Test_results")
    self.labelDBDir = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=13)
    self.labelDBDir.pack()
    self.labelDBDir.config(text = "DB-directory:")
    self.getDBDirIn = Button(frameLeft, 
                         text="Get DB directory", fg="red",
                         command=self.getDBDirectory)
    self.getDBDirIn.pack()
    self.text4 = Text(frameLeft,
                     bg="light blue",
                     height=1,
                     width=20)
    self.text4.pack()
    self.text4.insert(END, "part_RNAstructure/RNA_STRAND_data")
    self.getRNAPred = Button(frameLeft, 
                         text="Get RNAFold", fg="red",
                         command=self.getRNAPredFile)
    self.getRNAPred.pack()
    self.text8 = Text(frameLeft,
                     bg="light blue",
                     height=1,
                     width=20)
    self.text8.pack()
    self.text8.insert(END, "RNAFold")
    self.labelGeneID = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=10)
    self.labelGeneID.pack()
    self.labelGeneID.config(text = "Ref.-Seq ID:")
    self.text2 = Text(frameLeft,
                     bg="light green",
                     height=1,
                     width=15)
    self.text2.pack()
    self.text2.insert(END, "NC_007003.1")
    self.labelEMail = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=6)
    self.labelEMail.pack()
    self.labelEMail.config(text = "E-Mail:")
    self.text3 = Text(frameLeft,
                     bg="light green",
                     height=1,
                     width=20)
    self.text3.pack()
    self.pipStart = Button(frameLeft,
                         text="Start",
                         command=self.startPipeline)
    self.pipStart.pack()
    
    self.labelSep = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=20)
    self.labelSep.pack()
    self.labelSep.config(text = "____________________")

    # Compare
    self.labelpipeStart = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=10)
    self.labelpipeStart.pack()
    self.labelpipeStart.config(text = "Comparison:", font="Verdana 15 bold")
    self.labelFirstR = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=10)
    self.labelFirstR.pack()
    self.labelFirstR.config(text = "First report:")
    self.getDirInCompare = Button(frameLeft, 
                         text="Get first report", fg="red",
                         command=self.getInDirectoryCom)
    self.getDirInCompare.pack()
    self.text5 = Text(frameLeft,
                     bg="light blue",
                     height=1,
                     width=20)
    self.text5.pack()
    self.labelSecondR = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=12)
    self.labelSecondR.pack()
    self.labelSecondR.config(text = "Second report:")
    self.getOutDirCompare = Button(frameLeft, 
                         text="Get second report", fg="red",
                         command=self.getOutDirectoryCom)
    self.getOutDirCompare.pack()
    self.text6 = Text(frameLeft,
                     bg="light blue",
                     height=1,
                     width=20)
    self.text6.pack()
    self.compareVi = Button(frameLeft,
                         text="Compare Viruses",
                         command=self.compareV)
    self.compareVi.pack()

    self.labelSep2 = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=20)
    self.labelSep2.pack()
    self.labelSep2.config(text = "____________________")

    # Phyl.-Tree.
    self.labelpipeStart = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=7)
    self.labelpipeStart.pack()
    self.labelpipeStart.config(text = "Phyl.tree:", font="Verdana 15 bold")
    self.labelTree = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=12)
    self.labelTree.pack()
    self.labelTree.config(text = "Get FastA-File:")
    self.getDirInTree = Button(frameLeft, 
                         text="Get FastA-File", fg="red",
                         command=self.getInDirectoryTree)
    self.getDirInTree.pack()
    self.text7 = Text(frameLeft,
                     bg="light blue",
                     height=1,
                     width=20)
    self.text7.pack()
    self.treeComp = Button(frameLeft,
                         text="Compute Tree",
                         command=self.compTree)
    self.treeComp.pack()

  # Function to call the phyl.-tree part
  def compTree(self):
    err = open("errorLog.txt", 'w')

    fastaFile = self.text7.get(1.0, END)

    if fastaFile == "\n":
      self.label.config(text="Please select a FastA-File!")
      return

    checkclustal(err, self.label)
    # checkfasta(fastaFile, err, self.label)
    mutltSeqAl = runclustal(fastaFile, err, self.label)
    runphylogeny(err,self.label)
    mpconsense(err,self.label) 
    getconsensus(err,self.label) 
    drawtrees(err,self.label)

  # Different functions to get the directorys for result, db, etc.
  # First the text-field gets deleted
  # Second the dialogue is called for getting the folder/file from user
  # Third The folder/file-path is inserted into the text-field
  def getRNAPredFile(self):
    self.text8.delete(1.0, END)
    self.fileDir = tkFileDialog.askopenfilename()
    self.text8.insert(END, self.fileDir)

  def getInDirectoryTree(self):
    self.text7.delete(1.0, END)
    self.fileDir = tkFileDialog.askopenfilename(filetypes =
                [("FastA files","*.fasta"), ("FastA files", "*.fa")])
    self.text7.insert(END, self.fileDir)

  def getInDirectoryCom(self):
    self.text5.delete(1.0, END)
    self.fileDir = tkFileDialog.askopenfilename(filetypes = 
                [("PDF files", "*.pdf")])
    self.text5.insert(END, self.fileDir)

  def getOutDirectoryCom(self):
    self.text6.delete(1.0, END)
    self.fileDir = tkFileDialog.askopenfilename(filetypes = 
                [("PDF files", "*.pdf")])
    self.text6.insert(END, self.fileDir)

  def getDirectory(self):
    self.text1.delete(1.0, END)
    self.fileDir = tkFileDialog.askdirectory()
    self.text1.insert(END, self.fileDir)

  def getDBDirectory(self):
    self.text4.delete(1.0, END)
    self.dbDir = tkFileDialog.askdirectory()
    self.text4.insert(END, self.dbDir)

  # Function to start the comparison of two viruses
  def compareV(self):
    # error-file
    err = open("errorLog.txt", 'w')

    pathout = self.text1.get(1.0, END)
    path1 = self.text5.get(1.0, END)
    path2 = self.text6.get(1.0, END)

    # Tests for incompleteness (error-handling)
    if pathout == "\n":
      self.label.config(text="Please select an result-path!")
      return

    if path1 == "\n" or path2 == "\n":
      self.label.config(text="Please select both reports!")
      return

    compare(path1[:-1], path2[:-1], 
            pathout[:-1] + '/compareReport', 
            err, self.label)
    writeCompareReportAsPdf(pathout[:-1] + '/compareReport/', 
                          pathout[:-1] + '/compareReport/report_compared.pdf',
                          err, self.label)

  # The actual pipeline.
  # Get Sequence, predict ORFs, predict sec.struct and create a report
  def startPipeline(self):
    # error-file
    err = open("errorLog.txt", 'w')

    # getting user-input
    path = self.text1.get(1.0, END)
    GeneID = self.text2.get(1.0, END)
    email = self.text3.get(1.0, END)
    dbPath = self.text4.get(1.0, END)
    vName = self.textVName.get(1.0, END)
    rnaFold = self.text8.get(1.0, END)

    # Tests for incompleteness
    if path == "\n":
      self.label.config(text="Please select a result-path!")
      return
    if GeneID == "\n":
      self.label.config(text="Please enter a valid GeneID!")
      return
    if dbPath == "\n":
      self.label.config(text=
              "Please select a secondary structure prediction DB!")
      return

    # reading the input, getting sequence and error handling
    out = inputFromDB(GeneID, err, email, self.label)
    if out == -1:
      self.label.config(text="Wrong RefSeqID! Please enter a valid one!")
      return
    seqRecord2fasta(path[:-1] + "/test.fa", out, err, self.label)
    headers, seqs = readFasta(path[:-1] + "/test.fa", err)
    seq = seqs[0]

    # predicting ORFs and translating to protein
    orfs = predictORFS(seq, self.label, err)
    proteins = translateToProtein(orfs, self.label, err)
    domains = d.findDomains(proteins, path[:-1], self.label, err)
    if not domains:
      self.label.config(text="Something went wrong predicting the domains!")
      return

    # getting secondary structure
    mol = RNA_molecule(seqs[0], vName, "test", self.label, rnaFold)
    mol.db_parsed(dbPath[:-1] + '/', self.label)
    struc_db = parse_struc_db(mol.get_database())
    mol.search_rna_struc(struc_db, path[:-1], self.label)
    mol.writeTXT(path[:-1] + '/')

    # write PDF
    writeReportAsPdf(path[:-1] + '/',
                     path[:-1] + '/report.pdf', 
                     err, self.label)

    # Opens the pdf after the pipeline (only possible, if run as admin)
    if sys.platform.startswith('darwin'):
      os.system(path[:-1] + '/report.pdf')
    elif sys.platform.startswith('linux'):
      os.system(path[:-1] + '/report.pdf')
    elif sys.platform.startswith('win32'):
      os.startfile(path[:-1] + '/report.pdf')

# Runs the GUI
def main():
  root = Tk()
  app = App(root)
  root.mainloop()

if __name__ == "__main__":
    main()