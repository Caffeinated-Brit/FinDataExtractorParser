import pdfplumber
import os

def extract_text_from_pdf(file_path):
    # Extract text from PDF file using pdfplumber.
    print("Starting pdfPlumber process...")
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


if __name__ == "__main__":
    extract_text_from_pdf("C:/Users/lukas/Desktop/Capstone/FinDataExtractorParser/FinDataExtractorParser/examplePDFs/fromCameron/loan_statement.pdf")