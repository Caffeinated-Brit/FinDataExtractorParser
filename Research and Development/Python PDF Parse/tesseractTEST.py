# FIRST INSTALL DEPENDENCIES:
#   Read and follow "tesseractDependencies.md"

# Extracts text from an image based pdf
# Expect a somewhat long runtime

import pytesseract
from pdf2image import convert_from_path

# Be carefull of this file path
    # Use forward slashes as backslashes are used for escape characters
FILE_PATH = "Research and Development/Python PDF Parse/examplePDFs/scannedExample.pdf"

images = convert_from_path(FILE_PATH)
text = ""
for image in images:
    text += pytesseract.image_to_string(image)
print(text)