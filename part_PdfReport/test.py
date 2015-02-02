# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 12:39:47 2015

@author: maximilianhanussek
"""
import os
import sys
import writePdf as wPdf

from Tkinter import *


# Test
def main():
    # Error log
    r, err = os.pipe()
    err = open("./errorLog.txt", 'w')
    resultpath = sys.argv[1]
    outputpath = sys.argv[2]
    outputpath = outputpath + "report.pdf"

    # Starting UI
    root = Tk()
    frame = Frame(root)
    frame.pack()
    label = Label(frame,
                  width=100,
                  height=50)
    label.pack()

    # Start the report function
    # - resultpath with the txt files in it
    # - outputpath where to store the pdf file
    wPdf.writeReportAsPdf(resultpath, outputpath, err, label)

    root.mainloop()

if __name__ == "__main__":
    main()
