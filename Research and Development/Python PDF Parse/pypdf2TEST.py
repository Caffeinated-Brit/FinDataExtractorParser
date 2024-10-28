# Extracts text from text based pdf's

from PyPDF2 import PdfReader

reader = PdfReader("Research and Development/Python PDF Parse/examplePDFs/f1040.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()
print(text)
