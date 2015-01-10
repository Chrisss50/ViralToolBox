from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
    fp = file(path, 'rb')
    for page in PDFPage.get_pages(
            fp, set(), maxpages=0, password="", caching=True,
            check_extractable=True):
        PDFPageInterpreter(rsrcmgr, device).process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

if __name__ == "__main__":
    print convert_pdf_to_txt('test.pdf')
