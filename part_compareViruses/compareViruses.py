from convertPDF2txt import convert_pdf_to_txt as conv
import getInfo as info
from Bio.SeqUtils import GC
import sys
import os


__author__ = 'Mirjam Figaschewski'


def addTextToLabel(label, txt):
    currentLabelText = label["text"]
    currentLabelText += txt + '\n'
    label.config(text=currentLabelText)


#
# get domains' identifiers from dictionary of proteins
#
def getDomains(proteins):
    domains = []
    for val_protein in proteins.values():
        for val_domain in val_protein.values():
            # print val_domain
            if isinstance(val_domain, dict):
                ident = val_domain.get("identifier")
                if ident == "Identifier in the domain isn't available":
                    continue
                else:
                    domains.append(ident)
    return domains


#
# get positions of domains in RNA/DNA sequence from dictionary of proteins
#
def getPositions(proteins, err, name):
    position = {}
    for val_protein in proteins.values():
        start_nucleo = int(val_protein.get('Starting nucleotide position'))
        if start_nucleo == \
                "Starting nucleotide position in the predicted ORFs aren't available":
            return start_nucleo
        for val_domain in val_protein.values():
            if isinstance(val_domain, dict):
                start = val_domain.get("Starting aminoacid position")
                if not start == \
                        "Start AA position in the domain isn't available":
                    start = str(int(start) + start_nucleo)
                else:
                    start = -1
                    err.write("________________")
                    err.write("compareViruses:")
                    err.write("Start AA position in the domain isn't available" + " for " + name)
                end = val_domain.get("Ending aminoacid position")
                if not end == "End AA position in the domain isn't available":
                    end = str(int(end) + start_nucleo)
                else:
                    end = -1
                    err.write("________________")
                    err.write("compareViruses:")
                    err.write("End AA position in the domain isn't available" + " for " + name)
                ident = val_domain.get('identifier')
                position[ident] = [start, end]
    return position


#
# calculate  GC content
#
def GCcontent(seq1, seq2, name1, name2, err):
    if seq1 == "Sequence of the virus isn't available" and \
            seq2 == "Sequence of the virus isn't available":
        gc1 = "Sequence of " + name1 + " is not available"
        gc2 = "Sequence of " + name2 + " is not available"
        err.write("________________")
        err.write("compareViruses:")
        err.write("Sequences of both viruses are not available")
    elif seq1 == "Sequence of the virus isn't available":
        gc1 = "Sequence of " + name1 + " is not available"
        gc2 = GC(seq2)
        err.write("________________")
        err.write("compareViruses:")
        err.write("Sequence of " + name1 + " is not available")
    elif seq2 == "Sequence of the virus isn't available":
        gc1 = GC(seq1)
        gc2 = "Sequence of " + name2 + " is not available"
        err.write("________________")
        err.write("compareViruses:")
        err.write("Sequence of " + name2 + " is not available")
    else:
        gc1 = GC(seq1)
        gc2 = GC(seq2)
    return gc1, gc2


#
# get domains positions, common domains of the wiruses and percentual
# similarity of the viruses
#
def domainsInfo(proteins1, proteins2, name1, name2, err):
    domains1 = set(getDomains(proteins1))
    domainPositions1 = getPositions(proteins1, err, name1)
    if domainPositions1 == \
            "Starting nucleotide position in the predicted ORFs aren't available":
        err.write("________________")
        err.write("compareViruses:")
        err.write(domainPositions1 + " for " + name1)
    domains2 = set(getDomains(proteins2))
    domainPositions2 = getPositions(proteins2, err, name2)
    if domainPositions2 == \
            "Starting nucleotide position in the predicted ORFs aren't available":
        err.write("________________")
        err.write("compareViruses:")
        err.write(domainPositions1 + " for " + name2)
    commonDomains = domains1 & domains2
    allDomains = domains1 | domains2
    if not commonDomains:
        percentualSimilarity = 0
    else:
        percentualSimilarity = (len(commonDomains) / len(allDomains)) * 100
    return domainPositions1, domainPositions2, commonDomains, \
        percentualSimilarity


#
# main function to compare two viruses:
# get their sequences, secondary structure in dot-bracket, domains from pdfs
# calculae GC contents, common domains and the persentual similarity from that
#
def compare(pdf1, pdf2, result_path, err, label):
    file_path = result_path + '/compare_results.txt'
    if not os.path.exists(result_path):
        os.makedirs(result_path)
        addTextToLabel(label,  'Creating directory' + file_path)
    f = open(file_path, 'w+')
    addTextToLabel(label, 'Parsing ' + pdf1)
    pdf1 = conv(pdf1)
    pdf2 = conv(pdf2)
    pdfs = [pdf1, pdf2]
    for i in range(0, len(pdfs)):
        if pdfs[i].find("Virus Report", 0, 10) == -1:
            f.write("PDF" + str(i) + " was not generated by the VirusToolBox, stopped excecution")
            err.write("________________")
            err.write("compareViruses:")
            err.write("PDF" + str(i) + " was not generated by the VirusToolBox")
            return
    # get information from pdf files
    addTextToLabel(label, 'Get information from pdf1')
    name1, seq1, secstruct1, seq_energy1, numProteins1, proteins1 = \
        info.getInformation(pdf1, label)
    if name1 == "Name of the virus isn't available":
        name1 = "Virus 1"
    addTextToLabel(label, 'Get information from pdf2')
    name2, seq2, secstruct2, seq_energy2, numProteins2, proteins2 = \
        info.getInformation(pdf2, label)
    if name2 == "Name of the virus isn't available":
        name2 = "Virus 2"
    # calculate gc content of both sequences
    addTextToLabel(label, 'Calculating GC contents')
    gc1, gc2 = GCcontent(seq1, seq2, name1, name2, err)
    # get common domains, their positions in sequence and percentual similarity
    # of the viruses
    addTextToLabel(label, 'Calculating percentual similarity of domains')
    domainPositions1, domainPositions2, commonDomains, percentualSimilarity = \
        domainsInfo(proteins1, proteins2, name1, name2, err)
    # write results to file
    addTextToLabel(label, 'Writing results to ' + file_path)
    f.write('Sequences\n' + name1 + ': ' + seq1 + '\n' +
            name2 + ': ' + seq2 + '\n')
    f.write('Secondary structure:\n' + name1 + ' ' + secstruct1 + ' Energy: ' +
            seq_energy1 + '\n' + name2 + ' ' + secstruct2 +
            ' Energy: ' + seq_energy1 + '\n\n')
    f.write('GC content\n' + name1 + ': ' + str(gc1) + '\n' +
            name2 + ': ' + str(gc2) + '\n\n')
    f.write('Number of Proteins\n' + name1 + ': ' + str(numProteins1) + '\n' +
            name2 + ': ' + str(numProteins2) + '\n\n')
    f.write('Percentual similarity od domains: ' +
            str(percentualSimilarity) + '%\n\n')
    # write a table for common domains, its identifier, posistions in the
    # viruses, lengths in the viruses
    if commonDomains:
        first_column = len('Common domains')
        second_column = len('Position in ' + name1 + '  ')
        third_column = len('Position in ' + name2 + '  ')
        forth_column = len('Length in ' + name1 + ' ')
        fifth_column = len('Length in ' + name2 + ' ')
        f.write('Common domains|' +
                'Position in ' + name1 + '  |' +
                'Position in ' + name2 + '  |' +
                'Length in ' + name1 + ' ' + '|' + 'Length in ' + name2 + ' ' +
                '|\n')
        f.write('-' * first_column + '|' + '-' * second_column + '|' +
                '-' * third_column + '|' + '-' * forth_column + '|' +
                '-' * fifth_column + '|\n')
        domains = list(commonDomains)
        for i in range(0, len(commonDomains)):
            domain = domains[i]
            first = first_column - len(domain)
            if not domainPositions1 == \
                    "Starting nucleotide position in the predicted ORFs aren't available":
                positions1 = domainPositions1.get(domain)
                position1 = ':'.join(positions1)
                length1 = str(int(positions1[1]) - int(positions1[0]))
            else:
                position1 = "na"
                length1 = "na"
            sec = second_column - len(position1)
            forth = forth_column - len(length1)
            if not domainPositions1 == \
                    "Starting nucleotide position in the predicted ORFs aren't available":
                positions2 = domainPositions2.get(domain)
                position2 = ':'.join(positions2)
                length2 = str(int(positions2[1]) - int(positions2[0]))
            else:
                position2 = "na"
                length2 = "na"
            third = third_column - len(position2)
            fifth = fifth_column - len(length2)
            f.write(domain + ' ' * first + '|' +
                    position1 + ' ' * sec + '|' + position2 + ' ' * third + '|'
                    + length1 + ' ' * forth + '|' + length2 + ' ' * fifth +
                    '|\n')
    f.close()


if __name__ == "__main__":
    r, err = os.pipe()
    err = os.fdopen(err, 'w')
    pdf1 = sys.argv[1]
    pdf2 = sys.argv[2]
    result_path = sys.argv[3]
    compare(pdf1, pdf2, result_path, err, label)
