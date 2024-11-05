# FIRST INSTALL DEPENDENCIES:
    # pip install pdfplumber
    # pip install tabula-py
    # pip install pdf2image pytesseract
        # tesseract may need more configuration***

import pdfplumber
import tabula
from pdf2image import convert_from_path
import pytesseract

def extract_text_pdfplumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return pages

def extract_tables_tabula(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)
    return tables

def extract_text_tesseract(pdf_path):
    images = convert_from_path(pdf_path, dpi=300)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text
