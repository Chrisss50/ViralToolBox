from convertPDF2txt import convert_pdf_to_txt as conv
import getImagesFromPDF as parse
import getInfo as info
from Bio.SeqUtils import GC
import sys
import os


__author__ = 'Mirjam Figaschewski'


def getDomains(proteins):
    domains = []
    for val_protein in proteins.values():
        for val_domain in val_protein.values():
            if isinstance(val_domain, dict):
                domains.append(val_domain.get('identifier'))
    return domains


def compare(pdf1, pdf2, result_path):
    images_folder1 = result_path + '/images1'
    images_folder2 = result_path + '/images2'
    print 'Parsing ' + pdf1
    parse.get_pages(pdf1, images_folder1)
    pdf1 = conv(pdf1)
    print 'Parsing ' + pdf2
    parse.get_pages(pdf2, images_folder2)
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
    # domains1 = set(getDomains(proteins1))
    # domains2 = set(getDomains(proteins2))
    # similarDomains = domains1 & domains2
    # allDomains = domains1 | domains2
    # percentualSimilarity = (len(similarDomains) / len(allDomains)) * 100
    # write results to file
    print 'Writing results to file'
    f = open(result_path + '/results.txt', 'w+')
    f.write('Sequences\n' + name1 + ': ' + seq1 + '\n' +
            name2 + ': ' + seq2 + '\n')
    f.write('Secondary structure:\n' + name1 + ' ' + secstruct1 + ' Energy: ' +
            seq_energy1 + '\n' + name2 + ' ' + secstruct2 +
            ' Energy: ' + seq_energy1 + '\n\n')
    f.write('GC content\n' + name1 + ': ' + str(gc1) + '\n' +
            name2 + ': ' + str(gc2) + '\n\n')
    f.write('Number of Proteins\n' + name1 + ': ' + str(numProteins1) + '\n' +
            name2 + ': ' + str(numProteins2) + '\n\n')
    # f.write('Percentual similarity: ' +
    #         percentualSimilarity + '\n\n')
    # f.write('Common domains\n' + '\n'.join(list(similarDomains)))
    f.close()


if __name__ == "__main__":
    # pdf1 = sys.arg[0]
    # pdf1 = sys.arg[1]
    # result_path = sys.arg[2]
    # err = sys.arg[3]
    pdf1 = 'test.pdf'
    pdf2 = 'test.pdf'
    result_path = 'C:/Users/Mimi/Documents/GitHub/ViralToolBox/part_compareViruses/test'
    compare(pdf1, pdf2, result_path)
