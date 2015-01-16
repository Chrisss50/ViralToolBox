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
from writePdf import *
sys.path.append("part_compareViruses/")
from compareViruses import *

class App:
  txt = ""
  fileDir = " "

  def __init__(self, master):
    frame = Frame(master)
    frame.pack()
    self.getDirIn = Button(frame, 
                         text="Get directory", fg="red",
                         command=self.getDirectory)
    self.getDirIn.pack(side=LEFT)
    self.label = Label(frame, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       bg="light grey",
                       height=20,
                       width=100)
    self.label.pack(side = RIGHT)
    self.labelInput = Label(frame, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=10)
    self.labelInput.pack()
    self.labelInput.config(text = "Input Path:")
    self.text1 = Text(frame,
                     bg="light blue",
                     height=1,
                     width=20)
    self.text1.pack()
    self.labelGeneID = Label(frame, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=10)
    self.labelGeneID.pack()
    self.labelGeneID.config(text = "Gene ID:")
    self.text2 = Text(frame,
                     bg="light green",
                     height=1,
                     width=15)
    self.text2.pack()
    self.labelEMail = Label(frame, 
                       justify=LEFT,
                       anchor=SW,
                       fg="black",
                       height=1,
                       width=10)
    self.labelEMail.pack()
    self.labelEMail.config(text = "E-Mail:")
    self.text3 = Text(frame,
                     bg="light green",
                     height=1,
                     width=20)
    self.text3.pack()
    self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=frame.quit)
    self.button.pack(side=LEFT)
    self.slogan = Button(frame,
                         text="Input Start",
                         command=self.write_slogan)
    self.slogan.pack(side=LEFT)

  def getDirectory(self):
    self.fileDir = tkFileDialog.askdirectory()
    self.text1.insert(END, self.fileDir)

  def write_slogan(self):
    r, err = os.pipe()
    err = os.fdopen(err, 'w')
    path = self.text1.get(1.0, END)
    GeneID = self.text2.get(1.0, END)
    email = self.text3.get(1.0, END)
    out = inputFromDB(GeneID, err, email)
    # out = inputFromFile(path[:-1], err)
    seqRecord2fasta(path[:-1] + "/test.fa", out, err)
    headers, seqs = readFasta(path[:-1] + "/test.fa", err)
    seq = seqs[0]
    orfs = predictORFS(seq, err)
    proteins = translateToProtein(orfs, err)
    seq = {"sequence": getExampleProteinSequence(),
           "start": 1, "end": 1337}
    print findDomains([seq], path[:-1], err)
    for orf in orfs:
        self.txt += orf["sequence"]
    self.label.config(text=self.txt)
    mol = RNA_molecule(seqs[0], "HI-V", "test")
    mol.db_parsed("RNA_STRAND_data/")
    mol.print_rna_information()
    struc_db = parse_struc_db(mol.get_database())
    mol.search_rna_struc(struc_db)
    mol.print_rna_information()
    mol.writeTXT()
    resultpath = path[:-1]
    outputpath = path[:-1]
    outputpath += "report.pdf"
    writeReportAsPdf(resultpath, outputpath)
    compare(outputpath, outputpath, "./results", err, self.label)

root = Tk()
app = App(root)
root.mainloop()