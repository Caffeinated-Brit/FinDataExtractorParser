import pdfplumber
import os

# NOTE got rid of print outs for the the time being

def extract_text_from_pdf(file_path):
    # Extract text from PDF file using pdfplumber.
    extracted_data = ""
    if not os.path.exists(file_path):
        print(f"PDF file not found: {file_path}")
        return extracted_data

    # print(f"Extracting text from PDF: {file_path}")
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_data += text
    return extracted_data
