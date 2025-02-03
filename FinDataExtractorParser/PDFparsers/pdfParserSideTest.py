import pdfPlumber
import pyTesseract

FILE_PATH = "FinDataExtractorParser/examplePDFs/Simple Mock Data.pdf"

print("DATA: pdfplumber \n-----------------------------------------------")
print(pdfPlumber.extract_text_from_pdf(FILE_PATH))

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

print("DATA: pytesseract \n-----------------------------------------------")
print(pyTesseract.extract_content(FILE_PATH))