from PDFparsers import pdfPlumber, pyTesseract, linuxTest

parser_methods = {
    "pdfPlumber": pdfPlumber.extract_text_from_pdf,
    "pyTesseract": pyTesseract.extract_content,
    "linuxTest": linuxTest.linuxParse
}
