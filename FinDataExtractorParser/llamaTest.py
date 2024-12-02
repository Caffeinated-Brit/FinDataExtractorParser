# pip install llama-cpp-python
# use the download_llm.py file to download the LLM that is listed in LLAMA_MODEL_PATH

import os
import pdfplumber
from llama_cpp import Llama
import time

# Constants
# LLAMA_MODEL_PATH = "LLMs/Meta-Llama-3.1-8B-Instruct-Q5_K_L.gguf"
# LLAMA_MODEL_PATH = "LLMs/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"
LLAMA_MODEL_PATH = "LLMs/mistral-7b-instruct-v0.2.Q6_K.gguf"
PDF_FILE_PATH = "examplePDFs/Simple Mock Data.pdf"

# Initialize the Llama model
llm = Llama(
    model_path=LLAMA_MODEL_PATH,
    n_ctx=2048,  # Maximum context size for the model
    n_threads=8,  # Number of CPU threads
    n_gpu_layers=15  # Layers to assign to GPU. Start small (10), increase until approaching VRAM limit
)

def extract_text_from_pdf(file_path):
    # Extract text from PDF file using pdfplumber.
    extracted_data = []
    if not os.path.exists(file_path):
        print(f"PDF file not found: {file_path}")
        return extracted_data

    print(f"Extracting text from PDF: {file_path}")
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_data.append({"page_number": page.page_number, "text": text})
    return extracted_data

def process_text_with_llm(extracted_text):
    # Restrictive and clear prompt to avoid hallucinations.
    # I've tried just about every prompt I can think of, it still outputs random stuff.
    prompt = (
        # "You are an expert in analyzing financial documents. "
        # "Analyze the following text and extract meaningful financial information. "
        f"Follow the listed steps to analyze the following text and extract information. \n"
        f"Step 1: identify the key pieces of information in the text. "
        f"Do not print any text for this step. \n"
        f"Step 2: extract the information for each key. "
        f"Do not print any text for this step. \n"
        f"Step 3: format the extracted information into a JSON array. \n"
        # f"Analyze the following text and extract meaningful information.\n"
        # f"Do not make any assumptions, fabricate data, or respond with any information that was not provided to you.\n"
        # f"Return only the data that is explicitly present in the text, formatted as structured JSON.\n"
        f"Text for you to analyze:\n{extracted_text} \n"
        f"Return only your final answer in a JSON array.\n"

    )

    print("\nLLM processing...")
    start_time = time.time()  # Start timer
    print(prompt)

    # Add temperature and top_p for controlled, non-hallucinatory output
    response = llm(
        prompt,
        max_tokens=1024,  # More tokens = longer outputs capability
        temperature=0.1,
        top_p=1,
        top_k=1
        # All these variables aim to reduce randomness
        # For a visualization, refer to https://artefact2.github.io/llm-sampling/index.xhtml
    )

    end_time = time.time()  # End timer
    elapsed_time = end_time - start_time  # Calculate LLM calculation/response time
    print(f"LLM processing time: {elapsed_time:.2f} seconds")  # Output time

    return response["choices"][0]["text"].strip()

def main():
    # Extract text from the PDF
    extracted_data = extract_text_from_pdf(PDF_FILE_PATH)
    if not extracted_data:
        print("No text found in the PDF.")
        return

    extracted_text = " ".join([page["text"] for page in extracted_data])
    print("\n--- Extracted Text ---")
    print(extracted_text)

    # Process the text with the Llama model
    structured_data = process_text_with_llm(extracted_text)
    print("\n--- Structured Financial Data ---")
    print(structured_data)

if __name__ == "__main__":
    main()
