# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 00:45:06 2014

@author: maximilianhanussek
"""
import os
import sys
import datetime
import directoryFunctions as dF


from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch

# Print processing steps on the GUI
def addTextToLabel(label, txt):
    currentLabelText = label["text"]
    currentLabelText += txt + '\n'
    label.config(text = currentLabelText)

# Get an timestamp 
def getTimestamp():
    return str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

# Start writing the report
def writeReportAsPdf(resultpath, outputpath, err, label):
    doc = SimpleDocTemplate(outputpath, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=18)

    addTextToLabel(label, "Read in datapaths")
    
# Get the different files and parse the text out of them 
    Report = []
    Title = "Virus Report"
    Date = getTimestamp()
    VirusSecondaryStructureTxtPath = dF.findFileByName(resultpath, "sec_struct.txt")[0]
    VirusName = dF.findNextLineByKeyword(VirusSecondaryStructureTxtPath, "NAME:")[0]
    VirusSequence = dF.findNextLineByKeyword(VirusSecondaryStructureTxtPath, "SEQUENCE:")[0]
    VirusStructure = dF.findNextLineByKeyword(VirusSecondaryStructureTxtPath, "STRUCTURE:")[0]
    VirusEnergy = dF.findNextLineByKeyword(VirusSecondaryStructureTxtPath, "ENERGY:")[0]
    IMGSecondaryStructurePath = dF.findFileByName(resultpath, "sec_struct.ps")[0]
    IMGSecondaryStructure = Image(IMGSecondaryStructurePath, 3.5*inch, 3.5*inch)
    VirusDomainsTxtPath = dF.findFileByName(resultpath, "result.txt")[0]
    NoOfProteins = dF.findNextLineByKeyword(VirusDomainsTxtPath, "NumberOfProteins")[0]
    NoOfDomains = dF.findNextLineByKeyword(VirusDomainsTxtPath, "NumberOfDomains")
    AASequences = dF.findNextLineByKeyword(VirusDomainsTxtPath, "aminoAcidSequence")
    StartNucleotideInDNA =  dF.findNextLineByKeyword(VirusDomainsTxtPath, "startInDNASequence")
    EndNucleotideInDNA = dF.findNextLineByKeyword(VirusDomainsTxtPath, "endInDNASequence")
    StartAAInProtein = dF.findNextLineByKeyword(VirusDomainsTxtPath, "startInProteinSequence")
    EndAAInProtein = dF.findNextLineByKeyword(VirusDomainsTxtPath, "endInProteinSequence")
    DescriptionInDomain = dF.findNextLineByKeyword(VirusDomainsTxtPath, "description")
    IdentifierInDomain = dF.findNextLineByKeyword(VirusDomainsTxtPath, "identifier")
    IMGsProteinDomainsPath = dF.findFileByPattern(resultpath, "domain_graphic*")

# Define some styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='MyTitle', alignment=TA_CENTER))

    addTextToLabel(label, "Start creating the Report.pdf file")

# Set text onto the Pdf
    ptext = '<font name=Helvetica-Bold size=18>%s</font>' % Title
    Report.append(Paragraph(ptext, styles['MyTitle']))
    Report.append(Spacer(1, 12))

    ptext = '<font name=Helvetica size=12>%s</font>' % Date
    Report.append(Paragraph(ptext, styles["MyTitle"]))
    Report.append(Spacer(1, 12))

    ptext = '<font name=Helvetica-Bold size=14>%s</font>' % "Secondary structure results"
    Report.append(Paragraph(ptext, styles["Normal"]))
    Report.append(Spacer(1, 12))

    ptext = '<font name=Helvetica size=12>%s</font>' % "Virus name:"
    Report.append(Paragraph(ptext, styles["Normal"]))

    if(VirusName == "NAME: couldn't be found"):
        err.write("________________")
        err.write("Virus name isn't available")
        ptext = '<font name=Helvetica size=12>%s</font>' % "Name of the virus isn't available"
        Report.append(Paragraph(ptext, styles["Normal"]))
        Report.append(Spacer(1, 12))
    else:
        ptext = '<font name=Helvetica size=12>%s</font>' % VirusName
        Report.append(Paragraph(ptext, styles["Normal"]))
        Report.append(Spacer(1, 12))

    ptext = '<font name=Helvetica size=12>%s</font>' % "Sequence:"
    Report.append(Paragraph(ptext, styles["Normal"]))
    
    if(VirusSequence == "SEQUENCE: couldn't be found"):
            err.write("________________")
            err.write("Virus sequence isn't available")
            ptext = '<font name=Helvetica size=12>%s</font>' % "Sequence of the virus isn't available"
            Report.append(Paragraph(ptext, styles["Normal"]))
            Report.append(Spacer(1, 12))
    else:
        ptext = '<font name=Helvetica size=12>%s</font>' % VirusSequence
        Report.append(Paragraph(ptext, styles["Normal"]))
        Report.append(Spacer(1, 12))

    ptext = '<font name=Helvetica size=12>%s</font>' % "Structure in dot-bracket format:"
    Report.append(Paragraph(ptext, styles["Normal"]))

    if(VirusStructure == "STRUCTURE: couldn't be found"):
            err.write("________________")
            err.write("Virus structure isn't available")
            ptext = '<font name=Helvetica size=12>%s</font>' % "Structure of the virus isn't available"
            Report.append(Paragraph(ptext, styles["Normal"]))
            Report.append(Spacer(1, 12))
    else:
        ptext = '<font name=Helvetica size=12>%s</font>' % VirusStructure
        Report.append(Paragraph(ptext, styles["Normal"]))
        Report.append(Spacer(1, 12))

    ptext = '<font name=Helvetica size=12>%s</font>' % "Energy:"
    Report.append(Paragraph(ptext, styles["Normal"]))

    if(VirusEnergy == "ENERGY: couldn't be found"):
            err.write("________________")
            err.write("Energy of the secondary structure isn't available")
            ptext = '<font name=Helvetica size=12>%s</font>' % "SEnergy of the secondary structure isn't available"
            Report.append(Paragraph(ptext, styles["Normal"]))
            Report.append(Spacer(1, 12))
    else:
        ptext = '<font name=Helvetica size=12>%s</font>' % VirusEnergy
        Report.append(Paragraph(ptext, styles["Normal"]))
        Report.append(Spacer(1, 12))

    ptext = '<font name=Helvetica size=12>%s</font>' % "RNA-Structure:"
    Report.append(Paragraph(ptext, styles["Normal"]))
    Report.append(Spacer(1, 12))
    Report.append(IMGSecondaryStructure)
    Report.append(Spacer(1, 12))

    ptext = '<font name=Helvetica-Bold size=14>%s</font>' % "Virus Domain(s)"
    Report.append(Paragraph(ptext, styles["Normal"]))
    Report.append(Spacer(1, 12))
    
    ptext = '<font name=Helvetica size=12>%s</font>' % "Number of proteins:"
    Report.append(Paragraph(ptext, styles["Normal"]))
    
    if(NoOfProteins == "NumberOfProteins couldn't be found"):
            err.write("________________")
            err.write("Number of the proteins in the predicted ORFs aren't available")
            ptext = '<font name=Helvetica size=12>%s</font>' % "Number of the proteins in the predicted ORFs aren't available"
            Report.append(Paragraph(ptext, styles["Normal"]))
            Report.append(Spacer(1, 12))
    else:
        ptext = '<font name=Helvetica size=12>%s</font>' % NoOfProteins
        Report.append(Paragraph(ptext, styles["Normal"]))
        Report.append(Spacer(1, 12))
    
        for protein in range(0, int(NoOfProteins)):
            ptext = '<font name=Helvetica-Bold size=12>%s</font>' % "Protein " + str(protein+1)
            Report.append(Paragraph(ptext, styles["Normal"]))
            Report.append(Spacer(1, 12))
    
            ptext = '<font name=Helvetica size=12>%s</font>' % "Number of domains:"
            Report.append(Paragraph(ptext, styles["Normal"]))
    
            if(NoOfDomains[protein] == "NumberOfDomains couldn't be found"):
                err.write("________________")
                err.write("Number of the domains in the predicted ORFs aren't available")
                ptext = '<font name=Helvetica size=12>%s</font>' % "Number of the domains in the predicted ORFs aren't available"
                Report.append(Paragraph(ptext, styles["Normal"]))
                Report.append(Spacer(1, 12))
            else:
                ptext = '<font name=Helvetica size=12>%s</font>' % NoOfDomains[protein]
                Report.append(Paragraph(ptext, styles["Normal"]))
                Report.append(Spacer(1, 12))
    
            ptext = '<font name=Helvetica size=12>%s</font>' % "Aminoacidsequence:"
            Report.append(Paragraph(ptext, styles["Normal"]))
    
            if(AASequences[protein] == "aminoAcidSequence couldn't be found"):
                err.write("________________")
                err.write("Aminoacid sequence of the protein in the predicted ORFs aren't available")
                ptext = '<font name=Helvetica size=12>%s</font>' % "Aminoacid sequence of the protein in the predicted ORFs aren't available"
                Report.append(Paragraph(ptext, styles["Normal"]))
                Report.append(Spacer(1, 12))
            else:
                ptext = '<font name=Helvetica size=12>%s</font>' % AASequences[protein]
                Report.append(Paragraph(ptext, styles["Normal"]))
                Report.append(Spacer(1, 12))
    
            ptext = '<font name=Helvetica size=12>%s</font>' % "Starting nucleotide position:"
            Report.append(Paragraph(ptext, styles["Normal"]))
            
            if(StartNucleotideInDNA[protein] == "startInDNASequence couldn't be found"):
                err.write("________________")
                err.write("Number of the proteins in the predicted ORFs aren't available")
                ptext = '<font name=Helvetica size=12>%s</font>' % "Number of the proteins in the predicted ORFs aren't available"
                Report.append(Paragraph(ptext, styles["Normal"]))
                Report.append(Spacer(1, 12))
            else:
                ptext = '<font name=Helvetica size=12>%s</font>' % StartNucleotideInDNA[protein]
                Report.append(Paragraph(ptext, styles["Normal"]))
                Report.append(Spacer(1, 12))
    
            ptext = '<font name=Helvetica size=12>%s</font>' % "Ending nucleotide position:"
            Report.append(Paragraph(ptext, styles["Normal"]))
    
            if(EndNucleotideInDNA[protein] == "endInDNASequence couldn't be found"):
                err.write("________________")
                err.write("Number of the proteins in the predicted ORFs aren't available")
                ptext = '<font name=Helvetica size=12>%s</font>' % "Number of the proteins in the predicted ORFs aren't available"
                Report.append(Paragraph(ptext, styles["Normal"]))
                Report.append(Spacer(1, 12))
            else:
                ptext = '<font name=Helvetica size=12>%s</font>' % EndNucleotideInDNA[protein]
                Report.append(Paragraph(ptext, styles["Normal"]))
                Report.append(Spacer(1, 12))
    
            Report.append(Image(IMGsProteinDomainsPath[protein], 7*inch, 0.5*inch))
            Report.append(Spacer(1, 12))
            
            if(NoOfDomains[protein] == "NumberOfDomains couldn't be found"):
                err.write("________________")
                err.write("Number of the domains in the predicted ORFs aren't available and no domain information are available")
            else:                
                domain = int(NoOfDomains[protein])
                position = 0
        
                while domain > 0:
                    ptext = '<font name=Helvetica-Bold size=12>%s</font>' % "Domain " + str(position + 1)
                    Report.append(Paragraph(ptext, styles["Normal"]))
                    Report.append(Spacer(1, 12))
        
                    ptext = '<font name=Helvetica size=12>%s</font>' % "Starting aminoacid position:"
                    Report.append(Paragraph(ptext, styles["Normal"]))
        
                    if(StartAAInProtein[0] == "startInProteinSequence couldn't be found"):
                        err.write("________________")
                        err.write("Start AA position in the domain isn't available")
                        ptext = '<font name=Helvetica size=12>%s</font>' % "Start AA position in the domain isn't available"
                        Report.append(Paragraph(ptext, styles["Normal"]))
                        Report.append(Spacer(1, 12))
                    else:
                        ptext = '<font name=Helvetica size=12>%s</font>' % StartAAInProtein[0]
                        Report.append(Paragraph(ptext, styles["Normal"]))
                        Report.append(Spacer(1, 12))
                        del StartAAInProtein[0]
                    
                    ptext = '<font name=Helvetica size=12>%s</font>' % "Ending aminoacid position:"
                    Report.append(Paragraph(ptext, styles["Normal"]))
        
                    if(EndAAInProtein[0] == "endInProteinSequence couldn't be found"):
                        err.write("________________")
                        err.write("End AA position in the domain isn't available")
                        ptext = '<font name=Helvetica size=12>%s</font>' % "End AA position in the domain isn't available"
                        Report.append(Paragraph(ptext, styles["Normal"]))
                        Report.append(Spacer(1, 12))
                    else:
                        ptext = '<font name=Helvetica size=12>%s</font>' % EndAAInProtein[0]
                        Report.append(Paragraph(ptext, styles["Normal"]))
                        Report.append(Spacer(1, 12))
                        del EndAAInProtein[0]
                    
                    ptext = '<font name=Helvetica size=12>%s</font>' % "Domain description:"
                    Report.append(Paragraph(ptext, styles["Normal"]))
        
                    if(DescriptionInDomain[0] == "description couldn't be found"):
                        err.write("________________")
                        err.write("Description in the domain isn't available")
                        ptext = '<font name=Helvetica size=12>%s</font>' % "Description in the domain isn't available"
                        Report.append(Paragraph(ptext, styles["Normal"]))
                        Report.append(Spacer(1, 12))
                    else:
                        ptext = '<font name=Helvetica size=12>%s</font>' % DescriptionInDomain[0]
                        Report.append(Paragraph(ptext, styles["Normal"]))
                        Report.append(Spacer(1, 12))
                        del DescriptionInDomain[0]
                    
                    ptext = '<font name=Helvetica size=12>%s</font>' % "Identifier:"
                    Report.append(Paragraph(ptext, styles["Normal"]))
                    
                    if(IdentifierInDomain[0] == "identifier couldn't be found"):
                        err.write("________________")
                        err.write("Identifier in the domain isn't available")
                        ptext = '<font name=Helvetica size=12>%s</font>' % "Identifier in the domain isn't available"
                        Report.append(Paragraph(ptext, styles["Normal"]))
                        Report.append(Spacer(1, 12))
                    else:
                        ptext = '<font name=Helvetica size=12>%s</font>' % IdentifierInDomain[0]
                        Report.append(Paragraph(ptext, styles["Normal"]))
                        Report.append(Spacer(1, 12))
                        del IdentifierInDomain[0]
        
                    position += 1 
                    domain -= 1
            
    doc.build(Report)
    addTextToLabel(label, "Report.pdf has been created")
if __name__ == "__main__":
    r, err = os.pipe()
    err = os.fdopen(err, 'w')
    resultpath = sys.argv[1]
    outputpath = sys.argv[2]
    outputpath = outputpath + "report.pdf"
    writeReportAsPdf(resultpath, outputpath, err, label)
