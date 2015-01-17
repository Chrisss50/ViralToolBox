# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 09:07:15 2015

@author: maximilianhanussek
"""
import sys
import os
import datetime
import directoryFunctions as dF


from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus.flowables import Preformatted

# Print processing steps on the GUI
def addTextToLabel(label, txt):
    currentLabelText = label["text"]
    currentLabelText += txt + '\n'
    label.config(text = currentLabelText)

# Get an timestamp 
def getTimestamp():
    return str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

# Start writing the report
def writeCompareReportAsPdf(resultpath, outputpath, err, label):
    doc = SimpleDocTemplate(outputpath, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=18)

# Get the different files and parse the text out of them 
    Report = []
    Title = "Virus Report"
    SubTitle = "(Comparisons)"
    Date = getTimestamp()
    CompareTxtPath = dF.findFileByName(resultpath, "compare_results.txt")[0]
    CompareTxt = dF.readInFile(CompareTxtPath)

# Define some styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='MyTitle', alignment=TA_CENTER))

# Set text onto the Pdf
    ptext = '<font name=Helvetica-Bold size=18>%s</font>' % Title
    Report.append(Paragraph(ptext, styles['MyTitle']))
    Report.append(Spacer(1, 12))

    ptext = '<font name=Helvetica size=14>%s</font>' % SubTitle
    Report.append(Paragraph(ptext, styles['MyTitle']))
    Report.append(Spacer(1, 12))

    ptext = '<font name=Helvetica size=12>%s</font>' % Date
    Report.append(Paragraph(ptext, styles["MyTitle"]))
    Report.append(Spacer(1, 12))

    if(CompareTxt[0] == "The file doesn't exist"):
        err.write("________________")
        err.write("Write the comparison Pdf:")
        err.write("comparison.txt file doesn't exist")
        addTextToLabel(label, "Create Pdf file without statistics")
        ptext = '<font name=Helvetica-Bold size=16>%s</font>' % "The comparison file doesn't exist !"
        Report.append(Paragraph(ptext, styles["MyTitle"]))
    else:
        addTextToLabel(label, "Create Pdf file with comparison statistics")
        for i in range(0, len(CompareTxt)):
            ptext = CompareTxt[i]
            Report.append(Preformatted(ptext, styles['Code']))

    doc.build(Report)
if __name__ == "__main__":
    r, err = os.pipe()
    err = os.fdopen(err, 'w')
    resultpath = sys.argv[1]
    outputpath = sys.argv[2]
    outputpath = outputpath + "report_compared.pdf"
    writeReportAsPdf(resultpath, outputpath, err, label)
