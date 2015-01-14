# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 09:07:15 2015

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
from reportlab.platypus.flowables import Preformatted

def getTimestamp():
    return str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))


def writeReportAsPdf(resultpath, outputpath):
    doc = SimpleDocTemplate(outputpath, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=18)

    Report = []
    Title = "Virus Report"
    SubTitle = "(Comparisons)"
    Date = getTimestamp()
    CompareTxtPath = dF.findFileByName(resultpath, "compare_results.txt")[0]
    CompareTxt = dF.readInFile(CompareTxtPath)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='MyTitle', alignment=TA_CENTER))

    ptext = '<font name=Helvetica-Bold size=18>%s</font>' % Title
    Report.append(Paragraph(ptext, styles['MyTitle']))
    Report.append(Spacer(1, 12))

    ptext = '<font name=Helvetica size=14>%s</font>' % SubTitle
    Report.append(Paragraph(ptext, styles['MyTitle']))
    Report.append(Spacer(1, 12))

    ptext = '<font name=Helvetica size=12>%s</font>' % Date
    Report.append(Paragraph(ptext, styles["MyTitle"]))
    Report.append(Spacer(1, 12))

    for i in range(0, len(CompareTxt)):
        ptext = CompareTxt[i]
        Report.append(Preformatted(ptext, styles['Code']))

    doc.build(Report)
if __name__ == "__main__":
    resultpath = sys.argv[1]
    outputpath = sys.argv[2]
    outputpath = outputpath + "report_compared.pdf"
    writeReportAsPdf(resultpath, outputpath)
