import tkFileDialog
from Tkinter import *
sys.path.append("part_PredictAndTranslateORFs/")
from predictORFs import *
from translateToProtein import *
sys.path.append("part_DomainsInProtein/")
from domainsInProtein import *
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

class App:
  txt = ""
  fileDir = " "
  dbDir = " "

  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
    frameLeft = Frame(frame)
    frameLeft.pack(side=LEFT)
    frameRight = Frame(frame)
    frameRight.pack(side=RIGHT)

    self.label = Label(frameRight, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       bg="light grey",
                       height=30,
                       width=100)
    self.label.pack(side = RIGHT)

    self.labelInput = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=10)
    self.labelInput.pack()
    self.getDirIn = Button(frameLeft, 
                         text="Get directory", fg="red",
                         command=self.getDirectory)
    self.getDirIn.pack()
    self.labelInput.config(text = "Input Path:")
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
    self.getDBDirIn = Button(frameLeft, 
                         text="Get DB directory", fg="red",
                         command=self.getDBDirectory)
    self.getDBDirIn.pack()
    self.labelDBDir.config(text = "DB-directory:")
    self.text4 = Text(frameLeft,
                     bg="light green",
                     height=1,
                     width=20)
    self.text4.pack()
    self.labelGeneID = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=10)
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
                       width=10)
    self.labelEMail.pack()
    self.labelEMail.config(text = "E-Mail:")
    self.text3 = Text(frameLeft,
                     bg="light green",
                     height=1,
                     width=20)
    self.text3.pack()
    self.button = Button(frameLeft, 
                         text="QUIT", fg="red",
                         command=frame.quit)
    self.button.pack()
    self.slogan = Button(frameLeft,
                         text="Start",
                         command=self.write_slogan)
    self.slogan.pack()

    self.labelSep = Label(frameLeft, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=20)
    self.labelSep.pack()
    self.labelSep.config(text = "____________________")

    self.getDirInCompare = Button(frameLeft, 
                         text="Get first report", fg="red",
                         command=self.getInDirectoryCom)
    self.getDirInCompare.pack()
    self.text5 = Text(frameLeft,
                     bg="light blue",
                     height=1,
                     width=20)
    self.text5.pack()
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

  def getInDirectoryCom(self):
    self.text5.delete(1.0, END)
    self.fileDir = tkFileDialog.askopenfilename()
    self.text5.insert(END, self.fileDir)

  def getOutDirectoryCom(self):
    self.text6.delete(1.0, END)
    self.fileDir = tkFileDialog.askopenfilename()
    self.text6.insert(END, self.fileDir)

  def getDirectory(self):
    self.text1.delete(1.0, END)
    self.fileDir = tkFileDialog.askdirectory()
    self.text1.insert(END, self.fileDir)

  def getDBDirectory(self):
    self.text4.delete(1.0, END)
    self.dbDir = tkFileDialog.askdirectory()
    self.text4.insert(END, self.dbDir)

  def compareV(self):
    # pipe things
    r, err = os.pipe()
    err = os.fdopen(err, 'w')

    pathRes = self.text5.get(1.0, END)
    pathOut = self.text6.get(1.0, END)
    resultpath = pathRes[:-1]
    outputpath = pathOut[:-1]
    compare(outputpath, outputpath, pathRes[:-1], err, self.label)

  def write_slogan(self):
    # pipe things
    r, err = os.pipe()
    err = os.fdopen(err, 'w')

    # getting user-input
    path = self.text1.get(1.0, END)
    GeneID = self.text2.get(1.0, END)
    email = self.text3.get(1.0, END)
    dbPath = self.text4.get(1.0, END)

    # reading the input, getting sequence
    out = inputFromDB(GeneID, err, email)
    # out = inputFromFile(path[:-1], err)
    seqRecord2fasta(path[:-1] + "/test.fa", out, err)
    headers, seqs = readFasta(path[:-1] + "/test.fa", err)
    seq = seqs[0]

    # predicting ORFs and translating to protein
    orfs = predictORFS(seq, err)
    proteins = translateToProtein(orfs, err)
    seq = {"sequence": getExampleProteinSequence(),
           "start": 1, "end": 1337}
    print findDomains([seq], path[:-1], err)
    for orf in orfs:
        self.txt += orf["sequence"]
    self.label.config(text=self.txt)

    # getting secondary structure
    mol = RNA_molecule(seqs[0], "HI-V", "test")
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