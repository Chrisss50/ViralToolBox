# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 00:45:06 2014

@author: maximilianhanussek
"""
import sys
import datetime
import directoryFunctions as dF


from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


def getTimestamp():
    return str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))


def writeReportAsPdf(resultpath, outputpath):
    doc = SimpleDocTemplate(outputpath, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=18)

    Report = []
    Title = "Virus Report"
    Date = getTimestamp()
    IMGSecondaryStructurePath = dF.findFileByName(resultpath, "rna.ps")[0]
    IMGSecondaryStructure = Image(IMGSecondaryStructurePath, 4*inch, 4*inch)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='MyTitle', alignment=TA_CENTER))

    ptext = '<font name=Helvetica-Bold size=18>%s</font>' % Title
    Report.append(Paragraph(ptext, styles['MyTitle']))
    Report.append(Spacer(1, 12))
    ptext = '<font name=Helvetica size=12>%s</font>' % Date
    Report.append(Paragraph(ptext, styles["MyTitle"]))
    Report.append(Spacer(1, 12))
    ptext = '<font name=Helvetica size=12>%s</font>' % "RNA-Structure: "
    Report.append(Paragraph(ptext, styles["Normal"]))
    Report.append(Spacer(1, 12))
    Report.append(IMGSecondaryStructure)

    doc.build(Report)


if __name__ == "__main__":
    resultpath = sys.argv[1]
    outputpath = sys.argv[2]
    writeReportAsPdf(resultpath, outputpath)
