# FIRST INSTALL DEPENDENCY:
#   pip install pdfminer.six

# Highly recomended method we should look into -Lukas

# Extracts text from text based pdf's, is great for complicated formats. pdfminer is said to have a steep learning curve.

from pdfminer.high_level import extract_text

text = extract_text("Research and Development/Python PDF Parse/examplePDFs/f1040.pdf")
print(text)
