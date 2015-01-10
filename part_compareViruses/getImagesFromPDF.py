# by
# https://github.com/dpapathanasiou/pdfminer-layout-scanner/blob/master/layout_scanner.py
# changed by Mirjam Figaschewski

import sys
import os
from binascii import b2a_hex


###
# pdf-miner requirements
###

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTFigure, LTImage


def with_pdf(pdf_doc, fn, pdf_num, images_folder):
    """Open the pdf document, and apply the function, returning the results"""
    result = None
    try:
        # open the pdf file
        fp = open(pdf_doc, 'rb')
        # create a parser object associated with the file object
        parser = PDFParser(fp)
        # create a PDFDocument object that stores the document structure
        doc = PDFDocument(parser)
        # connect the parser and document objects
        parser.set_document(doc)
        if doc.is_extractable:
            # apply the function and return the result
            result = fn(doc=doc, pdf_num=pdf_num, images_folder=images_folder)
        # close the pdf file
        fp.close()
    except IOError:
        # the file doesn't exist or similar problem
        pass
    return result


def write_file(folder, filename, filedata, flags='w'):
    """Write the file data to the folder and filename combination
    (flags: 'w' for write text, 'wb' for write binary, use 'a' instead of 'w' for append)"""
    result = False
    if os.path.isdir(folder):
        try:
            file_obj = open(os.path.join(folder, filename), flags)
            file_obj.write(filedata)
            file_obj.close()
            result = True
        except IOError:
            pass
    return result


###
# Extracting Images
###

def determine_image_type(stream_first_4_bytes):
    """Find out the image file type based on the magic number comparison of the first 4 (or 2) bytes"""
    file_type = None
    bytes_as_hex = b2a_hex(stream_first_4_bytes)
    if bytes_as_hex.startswith('ffd8'):
        file_type = '.jpeg'
    elif bytes_as_hex == '89504e47':
        file_type = '.png'
    elif bytes_as_hex == '47494638':
        file_type = '.gif'
    elif bytes_as_hex.startswith('424d'):
        file_type = '.bmp'
    return file_type


def save_image(lt_image, filename, images_folder, pdf_num):
    """Try to save the image data from this LTImage object, and return the file name, if successful"""
    result = None
    if lt_image.stream:
        file_stream = lt_image.stream.get_rawdata()
        if file_stream:
            file_ext = determine_image_type(file_stream[0:4])
            if file_ext:
                name = list(filename)
                if os.path.exists(images_folder + filename + file_ext) and \
                        name[-1].isdigit():
                    num = int(name[-1]) + 1
                    filename = pdf_num + '_domain' + num
                filename = filename + file_ext
                if write_file(images_folder, filename, file_stream, flags='wb'):
                    result = filename
    return result


def parse_lt_objs(lt_objs, page_number, images_folder, pdf_num):
    """Iterate through the list of LT* objects and capture the text or image data contained in each"""
    text_content = []
    images = []
    for lt_obj in lt_objs:
        if isinstance(lt_obj, LTImage):
            # an image, so save it to the designated folder, and note its place
            # in the text
            images.append(lt_obj)
            # saved_file = save_image(lt_obj, page_number, images_folder)
        elif isinstance(lt_obj, LTFigure):
            # LTFigure objects are containers for other LT* objects, so recurse
            # through the children
            text_content.append(
                parse_lt_objs(
                    lt_obj, page_number, images_folder, pdf_num))
    for i in range(0, len(images)):
        if page_number == 1 and i == 0:
            filename = str(pdf_num) + '_sec_struct'
        else:
            filename = str(pdf_num) + '_domain' + str(i)
        saved_file = save_image(images[i], filename, images_folder, pdf_num)
        if saved_file:
                # use html style <img /> tag to mark the position of the image
                # within the text
                text_content.append(
                    '<img src="' + os.path.join(images_folder, saved_file) +
                    '" />')
        else:
            print >> sys.stderr, "error saving image on page", page_number, \
                filename


###
# Processing Pages
###

def _parse_pages(doc, images_folder, pdf_num):
    """With an open PDFDocument object, get the pages and parse each one
    [this is a higher-order function to be passed to with_pdf()]"""
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    text_content = []
    for i, page in enumerate(PDFPage.create_pages(doc)):
        interpreter.process_page(page)
        # receive the LTPage object for this page
        layout = device.get_result()
        # layout is an LTPage object which may contain child objects like
        # LTTextBox, LTFigure, LTImage, etc.
        text_content.append(
            parse_lt_objs(layout, (i + 1), images_folder, pdf_num))

    return text_content


def get_pages(pdf_doc, pdf_num, images_folder='/tmp'):
    """Process each of the pages in this pdf file and return a list of strings representing the text found in each page"""
    return with_pdf(pdf_doc, _parse_pages, pdf_num, images_folder)


if __name__ == "__main__":
    print get_pages(pdf_doc="051.pdf", images_folder='C:/Users/Mimi/Desktop/BioInfo/test/', pdf_num=1)
