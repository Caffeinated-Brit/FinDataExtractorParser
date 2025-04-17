from PDFparsers import pdfPlumber, pyTesseract, linux_pdftotext

parser_methods = {
    "pdfPlumber": pdfPlumber.extract_text_from_pdf,
    "pyTesseract": pyTesseract.extract_content,
    "linux_pdftotext": linux_pdftotext.linuxParse
}
