def getMetadata(substring, pdf, start=0, end=None):
    if end is None:
        end = len(pdf)
    substring_start = pdf.find(
        substring + '\n', start, end) + len(substring + '\n')
    substring_end = pdf.find('\n', substring_start)
    indices = pdf[substring_start: substring_end]
    return indices


def getSecStructInfo(pdf):
    # get sequence
    seq = getMetadata('dot_bracket', pdf)
    # get dot bracket notation for sequence
    secstruct_start = seq.end + len('\n')
    secstruct_end = pdf.find('\n', secstruct_start)
    secstruct = pdf[secstruct_start, secstruct_end]
    # get energy of secondary structure
    seq_energy_start = secstruct_end + len(seq)
    seq_energy_end = pdf.find('\n', seq_energy_start)
    seq_energy = pdf[seq_energy_start, seq_energy_end]
    return seq, secstruct, seq_energy


def getProteinInfo(pdf):
    numProteins = int(getMetadata('NumberOfProteins', pdf))
    if numProteins > 0:
        proteins = {}
        i = 1
        # for each protein get its aminoacid sequence and its domains
        while i <= numProteins:
            protein = 'Protein' + str(i)
            protein_start = pdf.find(protein) + len(protein + '\n')
            protein_end = pdf.find('\n\n', protein_start)
            # amino acid sequence
            aaSeq = getMetadata(
                'aminoAcidSequence', pdf, protein_start, protein_end)
            proteins[protein] = {'aminoAcidSequence': aaSeq}
            # start and end in DNA sequence
            startInDNASequence = getMetadata(
                'startInDNASequence', pdf, protein_start, protein_end)
            endInDNASequence = getMetadata(
                'endInDNASequence', pdf, protein_start, protein_end)
            proteins[protein].update(
                {'startInDNASequence': startInDNASequence})
            proteins[protein].update({'endInDNASequence': endInDNASequence})
            # number of domains
            numDomains = int(getMetadata(
                'NumberOfDomains', pdf, protein_start, protein_end))

            # get information for each domain (position, description, ...)
            if numDomains > 0:
                domains = {}
                j = 1
                while j <= numDomains:
                    domain = 'Domain' + str(j)
                    domain_start = pdf.find(
                        domain, protein_start, protein_end) + \
                        len(domain + '\n')
                    domain_end = pdf.find('\n\n', domain_start)
                    description = getMetadata(
                        'description', pdf, domain_start, domain_end)
                    startInProteinSequence = getMetadata(
                        'startInProteinSequence', pdf,
                        domain_start, domain_end)
                    endInProteinSequence = getMetadata(
                        'endInProteinSequence', pdf, domain_start, domain_end)
                    identifier = getMetadata(
                        'identifier', pdf, domain_start, domain_end)
                    domains[domain] = (
                        {'startInProteinSequence': startInProteinSequence},
                        {'endInProteinSequence': endInProteinSequence},
                        {'description': description},
                        {'identifier': identifier})
                    j += 1
            elif numDomains == 0:
                i += 1
            proteins[protein].update(domains)
            i += 1
        return numProteins, proteins


def getInformation(pdf):
    # get sequence, dot bracket notation for sequence and
    # energy of secondary structure
    seq, secstruct, seq_energy = getSecStructInfo(pdf)
    # get proteins and their domains
    numProteins, proteins = getProteinInfo(pdf)
    return seq, secstruct, seq_energy, numProteins, proteins
