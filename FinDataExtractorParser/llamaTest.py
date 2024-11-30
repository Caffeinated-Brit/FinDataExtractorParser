# pip install llama-cpp-python (added to requirements.txt so just run pip install -r requirements.txt)
# Have to run the download-llm.py file and ensure that it installs finance-llm.Q4_K_M.gguf in FinDataExtractor/LLMs/

import pdfplumber
from llama_cpp import Llama

# LLAMA_MODEL_PATH = "LLMs/finance-llm.Q4_K_M.gguf"
LLAMA_MODEL_PATH = "LLMs/Meta-Llama-3-8B-Instruct.Q5_K_S.gguf"
PDF_FILE_PATH = "examplePDFs/Simple Mock Data.pdf"  # Replace with your local PDF file path

# Initialize the Llama model
llm = Llama(
    model_path=LLAMA_MODEL_PATH,
    n_ctx=4096,  # Adjust based on your model's maximum context size
    n_threads=8,  # Number of threads to use
    n_gpu_layers=3  # Set GPU layers for acceleration if supported
)


def extract_text_from_pdf(file_path):
    # Extract text from the specified PDF file.
    extracted_data = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_data.append({"page_number": page.page_number, "text": text})
    return extracted_data


def process_text_with_llm(extracted_text):
    # Process the extracted text using the Llama model to extract financial data.
    # For testing, prompt can be changed depending on which document is being used
    prompt = (
        f"You are an expert in financial document analysis. "
        f"Parse the given text and respond with categorized JSON data."
        f"Do NOT make up any information."
        f"Return ONLY the JSON. Here is an example of JSON:\n"
        "{"
        f" \"Name\": \"[name]\", \"Date\":\"date\", \"Address\":\"address\" "
        "}"
        f"In the given example, the only information given was Name, Date, and Address."
        f"Text:\n{extracted_text}"
    )

    # Query the LLM
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
