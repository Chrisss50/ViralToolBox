import os
import sys
import pycurl
import urllib
import urllib2
import time
import json
import pickle
from StringIO import StringIO
from selenium import webdriver
from pyvirtualdisplay import Display
import PIL.Image
from Tkinter import *


__author__ = 'Felix Bartusch'


# An example Protein sequence
def getExampleProteinSequence():
    s = ("MAGAASPCANGCGPSAPSDAEVVHLCRSLEVGTVMTLFYSKKSQRPERKTFQVKLETRQI"
         "TWSRGADKIEGAIDIREIKEIRPGKTSRDFDRYQEDPAFRPDQSHCFVILYGMEFRLKTL"
         "SLQATSEDEVNMWIRGLTWLMEDTLQAATPLQIERWLRKQFYSVDRNREDRISAKDLKNM"
         "LSQVNYRVPNMRFLRERLTDLEQRTSDITYGQFAQLYRSLMYSAQKTMDLPFLEASALRA"
         "GERPELCRVSLPEFQQFLLEYQGELWAVDRLQVQEFMLSFLRDPLREIEEPYFFLDEFVT"
         "FLFSKENSIWNSQLDEVCPDTMNNPLSHYWISSSHNTYLTGDQFSSESSLEAYARCLRMG"
         "CRCIELDCWDGPDGMPVIYHGHTLTTKIKFSDVLHTIKEHAFVASEYPVILSIEDHCSIA"
         "QQRNMAQYFKKVLGDTLLTKPVDIAADGLPSPNQLKRKILIKHKKLAEGSAYEEVPTSVM"
         "YSENDISNSIKNGILYLEDPVNHEWYPHYFVLTSSKIYYSEETSSDQGNEDEEEPKEASG"
         "STELHSNEKWFHGKLGAGRDGRHIAERLLTEYCIETGAPDGSFLVRESETFVGDYTLSFW"
         "RNGKVQHCRIHSRQDAGTPKFFLTDNLVFDSLYDLITHYQQVPLRCNEFEMRLSEPVPQT"
         "NAHESKEWYHASLTRAQAEHMLMRVPRDGAFLVRKRNEPNSYAISFRAEGKIKHCRVQQE"
         "GQTVMLGNSEFDSLVDLISYYEKHPLYRKMKLRYPINEEALEKIGTAEPDYGALYEGRNP"
         "GFYVEANPMPTFKCAVKALFDYKAQREDELTFTKSAIIQNVEKQEGGWWRGDYGGKKQLW"
         "FPSNYVEEMVSPAALEPEREHLDENSPLGDLLRGVLDVPACQIAVRPEGKNNRLFVFSIS"
         "MASVAHWSLDVAADSQEELQDWVKKIREVAQTADARLTEGKMMERRKKIALELSELVVYC"
         "RPVPFDEEKIGTERACYRDMSSFPETKAEKYVNKAKGKKFLQYNRLQLSRIYPKGQRLDS"
         "SNYDPLPMWICGSQLVALNFQTPDKPMQMNQALFLAGGHCGYVLQPSVMRDEAFDPFDKS"
         "SLRGLEPCAICIEVLGARHLPKNGRGIVCPFVEIEVAGAEYDSIKQKTEFVVDNGLNPVW"
         "PAKPFHFQISNPEFAFLRFVVYEEDMFSDQNFLAQATFPVKGLKTGYRAVPLKNNYSEGL"
         "ELASLLVKIDVFPAKQENGDLSPFGGASLRERSCDASGPLFHGRAREGSFEARYQQPFED"
         "FRISQEHLADHFDGRDRRTPRRTRVNGDNRL")
    return s


# An example xml describing a job and containing the result_url
def getExampleXMLJobDescription():
    s = '<?xml version="1.0" encoding="UTF-8"?>\n\
        <jobs xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n\
              xmlns="http://pfam.xfam.org/"\n\
              xsi:schemaLocation="http://pfam.xfam.org/\n\
                                  http://pfam.xfam.org/static/documents/schemas/submission.xsd">\n\
          <job job_id="383F64A2-901A-11E4-9395-3A825F09777C">\n\
            <opened>2014-12-30T11:51:41</opened>\n\
            <result_url>http://pfam.xfam.org/search/sequence/resultset/383F64A2-901A-11E4-9395-3A825F09777C?output=xml</result_url>\n\
          </job>\n\
        </jobs>'

    return s


# An example json string describing protein domains
def getExampleJSONProteinDomainString():
    s = '{ "length" : "534",  \
        "regions" : [  \
            {  \
              "type" : "pfama",  \
              "text" : "Peptidase_S8",  \
              "colour" : "#2dcfff",  \
              "display": "true", \
              "startStyle" : "curved", \
              "endStyle" : "curved", \
              "start" : "159", \
              "end" : "361",  \
              "aliEnd" : "350",  \
              "aliStart" : "163"\
            }, \
            { \
              "type" : "pfama", \
              "text" : "PA", \
              "colour" : "#ff5353", \
              "display" : true, \
              "startStyle" : "jagged", \
              "endStyle" : "curved", \
              "start" : "388",\
              "end" : "469", \
              "aliEnd" : "469", \
              "aliStart" : "396"\
            } \
          ] \
        }'

    return s


def addTextToLabel(label, txt):
    # get the current text of the label
    currentLabelText = label['text']
    # Adding your current status of the tool. Dont forget the newline!
    currentLabelText += txt + '\n'
    # Writing it on the label
    label.config(text=currentLabelText)


# Extract the result_url of a xml job description
def extractResultURL(xml):
    # Split the xml string at the line breaks and remove whitespaces
    split = xml.split("\n")
    split = [s.strip() for s in split]

    # Get the result url
    result_url = None
    for s in split:
        if s.startswith("<result_url>"):
            result_url = s.split(">")[1].split("<")[0]
    return result_url


# Extract the job_id of a xml job description
def extractJobID(xml):
    # Split the xml string at the line breaks and remove whitespaces
    split = xml.split("\n")
    split = [s.strip() for s in split]

    # Get the result url
    job_id = None
    for s in split:
        if s.startswith("<job job_id"):
            job_id = s.split('"')[1]
    return job_id


# Query the pfam database for protein domains of the protein sequence.
# Return the result_url from there the result can be obtained.
def queryPfam(seq, label, err):
    result_url = None
    job_id = None
    while result_url is None or job_id is None:
        try:
            # Try it with pycurl
            b = StringIO()
            c = pycurl.Curl()
            c.setopt(c.URL, 'http://pfam.xfam.org/search/sequence')
            c.setopt(c.WRITEFUNCTION, b.write)
    
            # The form data
            formData = {'seq': seq, 'output': 'xml'}
            postfields = urllib.urlencode(formData)
            c.setopt(c.POSTFIELDS, postfields)
            c.setopt(c.FOLLOWLOCATION, True)
            c.perform()
    
            # for testing
            # HTTP response code, e.g. 200.
            #print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
            # Elapsed time for the transfer.
            #print('Status: %f' % c.getinfo(c.TOTAL_TIME))
    
            # testing
            xml = b.getvalue()
    
            result_url = extractResultURL(xml)
            job_id = extractJobID(xml)
            b.close()
            c.close()
        except BaseException as e:
            print "Error occured queriing pfam"
            err.write("________________")
            err.write("DomainsInProtein:")
            err.write("\tError quering pfam")
            return None, None
    return result_url, job_id


# Obtain the query result for a protein as a json string
def obtainQueryResult(protein, err):
    status = "RUN"
    # Try it with pycurl
    c = pycurl.Curl()
    url = "http://pfam.xfam.org/search/sequence/graphic/" + protein["job_id"]
    c.setopt(c.URL, url)
    # Check the response header
    # http://pfam.xfam.org/help#tabview=tab10
    if status not in ["RUN", "PEND"]:
        err.write("________________")
        err.write("DomainsInProtein:")
        err.write("\tError obtaining a query result from Pfam:")
        sys.exit()
    while(status == "RUN" or status == "PEND"):
        # obtain status
        buffer = StringIO()
        c.setopt(c.WRITEFUNCTION, buffer.write)
        c.perform()
        status = buffer.getvalue()
        if(status == "RUN"):
            time.sleep(1)
    c.close()
    # testing
    domainsJSON = status
    return domainsJSON


# Get the picture of domains
def getPictureOfDomain(json, baseDir):
    # use firefox to get page with javascript generated content
    url = "http://pfam.xfam.org/help/domain_graphics_example.html"
    # Use a virtual display
    display = Display(visible=0, size=(1600, 800))
    display.start()
    # Start the browser
    browser = webdriver.Firefox()
    # Load the site
    browser.get(url)
    # Set the json string
    browser.find_element_by_id("seq").clear()
    browser.find_element_by_id("seq").send_keys(json)
    time.sleep(2)

    # Generate the domain graphic
    browser.find_element_by_id("submit").click()
    time.sleep(3)

    # Take screenshot
    browser.save_screenshot(baseDir + 'screenshot.png')
    # Get WebElement position (position of domain graphic)
    dg = browser.find_elements_by_tag_name("div")[0]
    canvas = dg.find_element_by_id("anonymous_element_1")
    pos = canvas.location
    # Get WebElement dimension
    size = canvas.size
    # Crop WebElement image from page screenshot
    fp = open(baseDir + 'screenshot.png', 'r')
    im = PIL.Image.open(fp)
    box = (pos['x'], pos['y'],
           pos['x'] + size['width'], pos['y'] + size['height'])
    im = im.crop(box)
    # Delete the screenshot
    os.remove(baseDir + 'screenshot.png')
    # exit browser and display
    browser.quit()
    display.stop()
    return im


# Ensure that there is a network connection
def networkAvailable():
    try:
        urllib2.urlopen('http://74.125.228.100', timeout=1)
        return True
    except urllib2.URLError:
        pass
    return False


# Produce an output file summarising all findings
def saveResultsAsTextFile(domains, baseDir, err):
    # The seperator symbol
    sep = '\n'

    # Open the result file
    f = open(baseDir + "result.txt", 'w')

    # For each domain, write the important information
    f.write("NumberOfProteins" + sep + str(len(domains)) + '\n\n')
    i = 1
    for domain in domains:
        d = json.loads(domain['domains'])
        # Infos about the ORF
        f.write("Protein" + str(i) + '\n')
        f.write("NumberOfDomains" + sep + str(len(d['regions'])) + '\n')
        f.write("pathToImage" + sep + str(domain['domain_graphic_path']) + '\n')
        f.write("aminoAcidSequence" + sep + str(domain['sequence']) + '\n')
        f.write("startInDNASequence" + sep + str(domain['start']) + '\n')
        f.write("endInDNASequence" + sep + str(domain['end']) + '\n')

        # Infos about domains in the ORF
        # Read the json representation of the domains in the protein
        # For each domain a the ORF a list of domains exist
        d = json.loads(domain['domains'])
        j = 1
        for region in d['regions']:
            metadata = region['metadata']
            f.write("Domain" + str(j) + '\n')
            f.write("startInProteinSequence" + sep + metadata['start'] + '\n')
            f.write("endInProteinSequence" + sep + metadata['end'] + '\n')
            f.write("description" + sep + metadata['description'] + '\n')
            f.write("identifier" + sep + metadata['identifier'] + '\n')
            j += 1

        # Next
        f.write('\n')
        i += 1


# Find domains in the protein. To achieve this, query the pfam database.
# Save resulting pictures and json strings in the baseDir
def findDomains(proteins, baseDir, label, err):
    # Test internet connection
    if not networkAvailable():
        err.write("________________")
        err.write("DomainsInProtein:")
        err.write("\tNo network connection")
        sys.exit()

    # Ensure that the base directory is correct path
    if(baseDir[-1] != '/'):
        baseDir = baseDir + '/'

    # Make shure that the base dicrectory exists
    if not os.path.exists(baseDir):
        os.makedirs(baseDir)

    # This is a new list with proteins and results
    proteinsWithResults = []
    addTextToLabel(label, "Start finding domains for " + str(len(proteins)) + " proteins\n")
    count = 0
    # Make a query for each protein
    for protein in proteins:
        count += 1
        addTextToLabel(label, "Query pfam for protein " + str(count) + '\n')
        protein["result_url"], protein["job_id"] = queryPfam(protein["sequence"], label, err)
        # If we weren't able to query pfam, we cannot predict proteins
        if not protein["result_url"]:
            return None
        proteinsWithResults.append(protein)

    # Wait for 10 seconds
    time.sleep(20)
    # Try to open the result file
    try:
        path = baseDir + 'domains.txt'
        f = open(path, 'w')
    except IOError as e:
        err.write("________________")
        err.write("DomainsInProtein:")
        err.write("\tError opening new file for domains:")
        err.write("\tI/O error({0}): {1}".format(e.errno, e.strerror) + ": " + path)
        return None

    # Try to obtain the results
    count = 0
    domains = []
    for protein in proteinsWithResults:
        count += 1
        addTextToLabel(label, "Obtain protein domains from pfam for protein " + str(count) + '\n')
        # Get the json string describing the domains
        d = obtainQueryResult(protein, err)
        d = d[1:-1]
        protein["domains"] = d
        domains.append(protein)
        # Get a picture of the domains
        im = getPictureOfDomain(d, baseDir)
        # Save the picture and domains
        path = baseDir + 'domain_graphic' + str(count) + ".png"
        protein["domain_graphic_path"] = path
        try:
            im.save(protein["domain_graphic_path"])
        except IOError as e:
            err.write("________________")
            err.write("DomainsInProtein:")
            err.write("\tError saving domain graphics:")
            err.write("\tI/O error({0}): {1}".format(e.errno, e.strerror) + ": " + path)
            return None
        # Append the json string to file
        try:
            f.write(d + '\n')
        except IOError as e:
            err.write("________________")
            err.write("DomainsInProtein:")
            err.write("\tError writing domains to file:")
            err.write("\tI/O error({0}): {1}".format(e.errno, e.strerror) + ": " + path)
            return None
    # Write the results into a file
    saveResultsAsTextFile(domains, baseDir, err)

    # End
    addTextToLabel(label, "End finding domains!\n")
    return domains


# Test!
def main():
    # Error log
    r, err = os.pipe()
    err = os.fdopen(err, 'w')
    # The example protein sequence
    seq = {"sequence": getExampleProteinSequence(),
           "start": 1, "end": 1337}
           
    # Starting UI
    root = Tk()
    frame = Frame(root)
    frame.pack()
    label = Label(frame,
                  width = 100,
                  height = 10)
    label.pack()
    #root.mainloop()
    # Find domains in the protein
    findDomains([seq], ".", label, err)
    
    root.mainloop()

    # Generate result files for max
    #domains = pickle.load(open("./CacaoSwollenShootVirus/domains_dump.txt", "rb"))
    #saveResultsAsTextFile(domains, "./CacaoSwollenShootVirus/", err)


if __name__ == "__main__":
    main()