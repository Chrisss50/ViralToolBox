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
# sys.path.append("part_msa/")
# from msa_functions import *

class App:
  txt = ""
  fileDir = " "
  dbDir = " "
  logo = ""

  # This builds the UI
  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
    frameLeft = Frame(frame)
    frameLeft.pack(side=LEFT)
    frameRight = Frame(frame)
    frameRight.pack(side=RIGHT)
    self.logo = PhotoImage(file="Logo.gif")

    
    self.label = Label(frameRight, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       bg="light grey",
                       height=30,
                       width=100)
    self.label.pack(side = BOTTOM)
    self.labelLogo = Label(frameRight,
                       bg="light grey",
                       image = self.logo)
    self.labelLogo.pack()

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
    self.labelVName.config(text = "Virus-Name:")
    self.textVName = Text(frameLeft,
                     bg="light blue",
                     height=1,
                     width=20)
    self.textVName.pack()
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
    self.labelGeneID = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=8)
    self.labelGeneID.pack()
    self.labelGeneID.config(text = "Gene ID:")
    self.text2 = Text(frameLeft,
                     bg="light green",
                     height=1,
                     width=15)
    self.text2.pack()
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
    # self.button = Button(frameLeft, 
    #                      text="QUIT", fg="red",
    #                      command=frame.quit)
    # self.button.pack()
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

    self.text7 = Text(frameLeft,
                     bg="light blue",
                     height=1,
                     width=20)
    self.text7.pack()
    self.treeComp = Button(frameLeft,
                         text="Compute Tree",
                         command=self.compTree)
    self.treeComp.pack()

  # Theoretically tree building function (not tested)
  def compTree(self):
    pass
    # r, err = os.pipe()
    # err = os.fdopen(err, 'w')
    # fastaFile = self.text7.get(1.0, END)
    # checkfasta(fastaFile, err, self.label)
    # mutltSeqAl = runclustal(fastaFile, err, self.label)

  # Different functions to get the directorys
  def getInDirectoryCom(self):
    self.text5.delete(1.0, END)
    self.fileDir = tkFileDialog.askopenfilename(filetypes = [("PDF files", "*.pdf")])
    self.text5.insert(END, self.fileDir)

  def getOutDirectoryCom(self):
    self.text6.delete(1.0, END)
    self.fileDir = tkFileDialog.askopenfilename(filetypes = [("PDF files", "*.pdf")])
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
    # pipe things
    r, err = os.pipe()
    err = os.fdopen(err, 'w')

    pathout = self.text1.get(1.0, END)
    path1 = self.text5.get(1.0, END)
    path2 = self.text6.get(1.0, END)

    # Tests for incompleteness
    if pathout == "\n":
      self.label.config(text="Please select an result-path!")
      return

    if path1 == "\n" or path2 == "\n":
      self.label.config(text="Please select both reports!")
      return

    compare(path1[:-1], path2[:-1], pathout[:-1] + '/compareReport', err, self.label)
    writeCompareReportAsPdf(pathout[:-1] + '/compareReport/', pathout[:-1] + '/compareReport/report_compared.pdf', err, self.label)

  def startPipeline(self):
    # pipe things
    r, err = os.pipe()
    err = os.fdopen(err, 'w')

    # getting user-input
    path = self.text1.get(1.0, END)
    GeneID = self.text2.get(1.0, END)
    email = self.text3.get(1.0, END)
    dbPath = self.text4.get(1.0, END)
    vName = self.textVName.get(1.0, END)

    # Tests for incompleteness
    if path == "\n":
      self.label.config(text="Please select a result-path!")
      return

    if GeneID == "\n":
      self.label.config(text="Please enter a valid GeneID!")
      return

    if dbPath == "\n":
      self.label.config(text="Please select a secondary structure prediction DB!")
      return

    # reading the input, getting sequence
    out = inputFromDB(GeneID, err, email, self.label)
    # out = inputFromFile(path[:-1], err)
    seqRecord2fasta(path[:-1] + "/test.fa", out, err, self.label)
    headers, seqs = readFasta(path[:-1] + "/test.fa", err)
    seq = seqs[0]

    # predicting ORFs and translating to protein
    orfs = predictORFS(seq, self.label, err)
    proteins = translateToProtein(orfs, self.label, err)
    d.findDomains(proteins, path[:-1], self.label, err)
    # for orf in orfs:
    #     self.txt += orf["sequence"]
    # self.label.config(text=self.txt)

    # getting secondary structure
    mol = RNA_molecule(seqs[0], vName, "test")
    mol.db_parsed(dbPath[:-1] + '/')
    struc_db = parse_struc_db(mol.get_database())
    mol.search_rna_struc(struc_db, path[:-1])
    mol.writeTXT(path[:-1] + '/')

    # write PDF
    # writeReportAsPdf(path[:-1] + '/', path[:-1] + '/', err, self.label)
    writeReportAsPdf(path[:-1] + '/', path[:-1] + '/report.pdf', err, self.label)

root = Tk()
app = App(root)
root.mainloop()