# pip install tensorflow
# pip install tf-keras

import json
import sys
from AI_categorizer import extract_text_pdfplumber, extract_tables_tabula, extract_text_tesseract
from PDF_to_JSON import categorize_text, extract_entities

def process_pdf_to_categorized_json(pdf_path):
    # Extract text data from PDF
    print("Extracting text data from PDF...")
    text_data = extract_text_pdfplumber(pdf_path)

    if not text_data:  # Fallback to OCR if no text was found
        print("No text detected, using OCR...")
        text_data = extract_text_tesseract(pdf_path)

    # Extract table data (if available)
    print("Extracting tables from PDF...")
    table_data = extract_tables_tabula(pdf_path)

    # Prepare JSON structure
    categorized_data = []

    # Categorize each text entry
    print("Categorizing text entries...")
    for page_text in text_data:
        for line in page_text.splitlines():
            if line.strip():  # Ignore empty lines
                category = categorize_text(line)[0]['label']
                entities = extract_entities(line)
                categorized_data.append({
                    "text": line,
                    "category": category,
                    "entities": entities
                })

    # Categorize each table entry
    print("Categorizing table entries...")
    for table in table_data:
        for row in table:
            for cell in row:
                if isinstance(cell, str) and cell.strip():  # Process text cells
                    category = categorize_text(cell)[0]['label']
                    entities = extract_entities(cell)
                    categorized_data.append({
                        "text": cell,
                        "category": category,
                        "entities": entities
                    })

    return categorized_data

def main():
    # if len(sys.argv) != 2:
    #     print("Usage: python main.py <path_to_pdf>")
    #     sys.exit(1)

    # pdf_path = sys.argv[1]
    pdf_path = "C:/Users/lukas/Desktop/Current GIT/FinDataExtractorParser/Research and Development/Python PDF Parse/examplePDFs/f1040.pdf"
    categorized_data = process_pdf_to_categorized_json(pdf_path)

    # Save the categorized data to JSON
    output_file = pdf_path.replace('.pdf', '_categorized.json')
    with open(output_file, 'w') as f:
        json.dump(categorized_data, f, indent=4)
    print(f"Categorized data saved to {output_file}")

if __name__ == "__main__":
    main()
