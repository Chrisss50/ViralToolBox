import sys
import os
sys.path.append("part_DomainsInProtein")
sys.path.append("part_PredictAndTranslateORFs")
import domainsInProtein
import predictORFs
import translateToProtein
import pickle


def main():
    r, err = os.pipe()
    err = os.fdopen(err, 'w')

    virus1 = "./test_sequences/acuminataVietnam.fasta"
    virus2 = "./test_sequences/CacaoSwollenShootVirus.fasta"

    virus1_headers, virus1_seqs = predictORFs.readFasta(virus1, err)
    virus1_seq = virus1_seqs[0]
    virus2_headers, virus2_seqs = predictORFs.readFasta(virus2, err)
    virus2_seq = virus2_seqs[0]

    # Find ORFs
    virus1_orfs =  predictORFs.predictORFS(virus1_seq, err)
    virus2_orfs =  predictORFs.predictORFS(virus2_seq, err)

    #print virus1_orfs
    #print virus2_orfs

    # Translate ORFs to proteins
    virus1_proteins = translateToProtein.translateToProtein(virus1_orfs, err)
    virus2_proteins = translateToProtein.translateToProtein(virus2_orfs, err)

    #print virus1_proteins
    print virus2_proteins

    # Find domains for the proteins
    #virus1_domains = domainsInProtein.findDomains(virus1_proteins, "./part_DomainsInProtein/acuminataVietnam/", err)
    virus2_domains = domainsInProtein.findDomains(virus2_proteins, "./part_DomainsInProtein/CacaoSwollenShootVirus/", err)

    # Dump the domains objects to disc
    #pickle.dump(virus1_domains, open("./part_DomainsInProtein/acuminataVietnam/domains_dump.txt", 'w'))
    pickle.dump(virus2_domains, open("./part_DomainsInProtein/CacaoSwollenShootVirus/domains_dump.txt", 'w'))

    # Try to load the dump
    #virus1_domains_dump = pickle.load(open("./part_DomainsInProtein/acuminataVietnam/domains_dump.txt", "rb"))
    virus2_domains_dump = pickle.load(open("./part_DomainsInProtein/CacaoSwollenShootVirus/domains_dump.txt", "rb"))

    # Test the dump
    #print virus1_domains_dump
    print virus2_domains_dump
    
if __name__ == "__main__":
    main()