# Extracts text from first page of text based pdf's

from pypdf import PdfReader

reader = PdfReader("Research and Development/Python PDF Parse/examplePDFs/f1040.pdf")
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()

print(f"Number of pages: {number_of_pages}")
print(text)