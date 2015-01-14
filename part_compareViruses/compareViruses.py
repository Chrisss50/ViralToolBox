from convertPDF2txt import convert_pdf_to_txt as conv
import getInfo as info
from Bio.SeqUtils import GC
import sys
import os


__author__ = 'Mirjam Figaschewski'


#
# get domains' identifiers from dictionary of proteins
#
def getDomains(proteins):
    domains = []
    for val_protein in proteins.values():
        for val_domain in val_protein.values():
            # print val_domain
            if isinstance(val_domain, dict):
                domains.append(val_domain.get('identifier'))
    return domains


#
# get positions of domains in RNA/DNA sequence from dictionary of proteins
#
def getPositions(proteins):
    position = {}
    for val_protein in proteins.values():
        start_nucleo = int(val_protein.get('Starting nucleotide position'))
        for val_domain in val_protein.values():
            if isinstance(val_domain, dict):
                start = str(int(val_domain.get('Starting aminoacid position'))
                            + start_nucleo)
                end = str(int(val_domain.get('Ending aminoacid position'))
                          + start_nucleo)
                ident = val_domain.get('identifier')
                position[ident] = [start, end]
    return position


#
# main function to compare two viruses:
# get their sequences, secondary structure in dot-bracket, domains from pdfs
# calculae GC contents, common domains and the persentual similarity from that
#
def compare(pdf1, pdf2, result_path, err):
    paths = [pdf1, pdf2, result_path]
    # possible errors for paths: path is empty or does not exist
    for i in range(0, len(paths)):
        if i == 0:
            path = "pdf1"
        elif i == 1:
            path = "pdf2"
        else:
            path = "location to save results"
        if paths[i] == "":
            err.write("________________")
            err.write("compareViruses:")
            err.write("\tPath to " + path + " is missing")
            print("Stopped execution, look up the error in the error-log")
            sys.exit()
        elif not os.path.exists(paths[i]) and (i == 0 or i == 1):
            err.write("________________")
            err.write("compareViruses:")
            err.write("\tPath to " + path + " for first virus does not exist")
            print("Stopped execution, look up the error in the error-log")
            sys.exit()
    if not os.path.exists(result_path):
        print "Creating path to results: " + result_path
        os.makedirs(result_path)
    print 'Parsing ' + pdf1
    pdf1 = conv(pdf1)
    print 'Parsing ' + pdf2
    pdf2 = conv(pdf2)
    # get information from pdf files
    print 'Get information from pdf1'
    name1, seq1, secstruct1, seq_energy1, numProteins1, proteins1 = \
        info.getInformation(pdf1)
    print 'Get information from pdf2'
    name2, seq2, secstruct2, seq_energy2, numProteins2, proteins2 = \
        info.getInformation(pdf2)
    # calculate gc content of both sequences
    print 'Calculating GC contents'
    gc1 = GC(seq1)
    gc2 = GC(seq2)
    # get common domains, their positions in sequence and percentual similarity
    # of the viruses
    print 'Calculating percentual similarity'
    domains1 = set(getDomains(proteins1))
    domainPositions1 = getPositions(proteins1)
    domains2 = set(getDomains(proteins2))
    domainPositions2 = getPositions(proteins2)
    commonDomains = domains1 & domains2
    allDomains = domains1 | domains2
    if not commonDomains:
        percentualSimilarity = 0
    else:
        percentualSimilarity = (len(commonDomains) / len(allDomains)) * 100
    # write results to file
    file_path = result_path + '/compare_results.txt'
    if not os.path.exists(file_path):
        print 'Creating directory' + file_path
        print 'Writing results to ' + file_path
    else:
        print 'Overwriting ' + file_path
    f = open(file_path, 'w+')
    f.write('Sequences\n' + name1 + ': ' + seq1 + '\n' +
            name2 + ': ' + seq2 + '\n')
    f.write('Secondary structure:\n' + name1 + ' ' + secstruct1 + ' Energy: ' +
            seq_energy1 + '\n' + name2 + ' ' + secstruct2 +
            ' Energy: ' + seq_energy1 + '\n\n')
    f.write('GC content\n' + name1 + ': ' + str(gc1) + '\n' +
            name2 + ': ' + str(gc2) + '\n\n')
    f.write('Number of Proteins\n' + name1 + ': ' + str(numProteins1) + '\n' +
            name2 + ': ' + str(numProteins2) + '\n\n')
    f.write('Percentual similarity: ' +
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
            positions1 = domainPositions1.get(domain)
            position1 = ':'.join(positions1)
            sec = second_column - len(position1)
            positions2 = domainPositions2.get(domain)
            position2 = ':'.join(positions2)
            third = third_column - len(position2)
            length1 = str(int(positions1[1]) - int(positions1[0]))
            forth = forth_column - len(length1)
            length2 = str(int(positions2[1]) - int(positions2[0]))
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
    compare(pdf1, pdf2, result_path, err)
