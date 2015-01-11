from convertPDF2txt import convert_pdf_to_txt as conv
import getInfo as info
from Bio.SeqUtils import GC
import sys
import os


__author__ = 'Mirjam Figaschewski'


def getDomains(proteins):
    domains = []
    for val_protein in proteins.values():
        for val_domain in val_protein.values():
            # print val_domain
            if isinstance(val_domain, dict):
                domains.append(val_domain.get('identifier'))
    return domains


def getPositions(proteins):
    position = {}
    for val_protein in proteins.values():
        start_nucleo = val_protein.get('Starting nucleotide position')
        end_nucleo = val_protein.get('Ending nucleotide position')
        for val_domain in val_protein.values():
            if isinstance(val_domain, dict):
                start = val_domain.get('Starting aminoacid position') + \
                    start_nucleo
                end = val_domain.get('Ending aminoacid position') + end_nucleo
                ident = val_domain.get('identifier')
                position[ident] = [start, end]
    return position


def compare(pdf1, pdf2, result_path, err):
    if pdf1 == "":
        err.write("________________")
        err.write("compareViruses:")
        err.write("\tPath to pdf for first virus is missing")
        sys.exit()
    if pdf2 == "":
        err.write("________________")
        err.write("compareViruses:")
        err.write("\tPath to pdf for second virus is missing")
        sys.exit()
    if result_path == "":
        err.write("________________")
        err.write("compareViruses:")
        err.write(
            "\tPath to location, where results should be saved, is missing")
        sys.exit()
    if not os.path.exists(pdf1):
        err.write("________________")
        err.write("compareViruses:")
        err.write("\tPath to pdf for first virus does not exist")
        sys.exit()
    if not os.path.exists(pdf2):
        err.write("________________")
        err.write("compareViruses:")
        err.write("\tPath to pdf for second virus does not exist")
        sys.exit()
    if not os.path.exists(result_path):
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
    # get similar domains and percentual similarity
    print 'Calculating percentual similarity'
    domains1 = set(getDomains(proteins1))
    domainPositions1 = getPositions(proteins1)
    domains2 = set(getDomains(proteins2))
    domainPositions2 = getPositions(proteins2)
    similarDomains = domains1 & domains2
    allDomains = domains1 | domains2
    percentualSimilarity = (len(similarDomains) / len(allDomains)) * 100
    # write results to file
    file_path = result_path + '/results.txt'
    if not os.path.exists(file_path):
        print 'Creating directory' + file_path
    else:
        print 'Overwriting ' + file_path
    print 'Writing results to ' + file_path
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
    first_column = len('Common domains')
    second_column = len('Position in ' + name1 + ' ')
    third_column = len('Position in ' + name2 + ' ')
    f.write('Common domains|' + 'Position in ' + name1 + ' '
            + '|' + 'Position in ' + name2 + ' |\n')
    f.write('-' * first_column + '|' + '-' * second_column + '|' +
            '-' * third_column + '|' + '\n')
    domains = list(similarDomains)
    for i in range(0, len(similarDomains)):
        domain = domains[i]
        first = first_column - len(domain)
        position1 = ':'.join(domainPositions1.get(domain))
        sec = second_column - len(position1)
        position2 = ':'.join(domainPositions2.get(domain))
        third = third_column - len(position2)
        f.write(domain + ' ' * first + '|' + position1 + ' ' * sec
                + '|' + position2 + ' ' * third + '|\n')
    f.close()


if __name__ == "__main__":
    r, err = os.pipe()
    err = os.fdopen(err, 'w')
    pdf1 = sys.argv[1]
    pdf2 = sys.argv[2]
    result_path = sys.argv[3]
    compare(pdf1, pdf2, result_path, err)
