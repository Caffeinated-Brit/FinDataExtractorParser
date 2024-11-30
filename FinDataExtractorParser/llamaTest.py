# pip install llama-cpp-python
# make sure you download the LLM to FinDataExtractorParser/LLMs/finance-llm.Q4_K_M.gguf

import pdfplumber
from llama_cpp import Llama

# Path to your Finance LLM GGUF model
LLAMA_MODEL_PATH = "LLMs/finance-llm.Q4_K_M.gguf"

# Path to the PDF file for testing
PDF_FILE_PATH = "examplePDFs/Simple Mock Data.pdf"  # Replace with your local PDF file path

# Initialize the Llama model
llm = Llama(
    model_path=LLAMA_MODEL_PATH,
    n_ctx=4096,  # Adjust based on your model's maximum context size
    n_threads=8,  # Number of threads to use
    n_gpu_layers=3  # Set GPU layers for acceleration if supported
)


def extract_text_from_pdf(file_path):
    """
    Extract text from the specified PDF file.
    """
    extracted_data = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_data.append({"page_number": page.page_number, "text": text})
    return extracted_data


def process_text_with_llm(extracted_text):
    """
    Process the extracted text using the Llama model to extract financial data.
    """
    # for testing, prompt can be changed depending on which document is being used
    prompt = (
        f"You are an expert in financial document analysis. "
        f"Extract the following key information from the provided text:\n"
        f"1. Name\n"
        f"2. Date\n"
        f"3. Address\n"
        f"4. Spouse's name\n"
        f"5. Any other relevant data"
        f"Text:\n{extracted_text}"
    )

    # Query the Llama model
    response = llm(prompt, max_tokens=1024)  # Adjust max_tokens as needed
    return response["choices"][0]["text"].strip()


def main():
    if not PDF_FILE_PATH:
        print("Please specify a valid PDF file path in the `PDF_FILE_PATH` variable.")
        return

    print(f"Processing file: {PDF_FILE_PATH}")

    # Extract text from the PDF
    extracted_data = extract_text_from_pdf(PDF_FILE_PATH)
    if not extracted_data:
        print("No text found in the PDF file.")
        return

    # Combine all extracted text
    extracted_text = " ".join([page["text"] for page in extracted_data])
    print("\n--- Extracted Text ---")
    print(extracted_text)

    # Process the text with Llama model
    structured_data = process_text_with_llm(extracted_text)
    print("\n--- Structured Financial Data ---")
    print(structured_data)


if __name__ == "__main__":
    main()
