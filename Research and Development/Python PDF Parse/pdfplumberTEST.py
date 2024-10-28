# Extracts the first character’s information from the page outputs in json. May be usefull when dealing with complicated layouts or text that is not parsing correctly.

import pdfplumber

with pdfplumber.open("Research and Development/Python PDF Parse/examplePDFs/f1040.pdf") as pdf:
    first_page = pdf.pages[0]
    print(first_page.chars[0])