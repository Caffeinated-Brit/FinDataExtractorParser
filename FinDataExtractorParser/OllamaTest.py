# go to the ollama github page download for windows
# to download the model find it on ollama's site(https://ollama.com/search) and in the command line run "ollama run "name of model""
# example of getting a model "ollama run llama3.1:8b"
# dont forget to type the size of the model in addition to the name


#tested models
#llama3.1:8b works well
#qwen2.5:14b works very very well giving basically only valid json on its own
#llama3.2:3b sucks
#qwen2.5-coder:3b great amazing, as far as tested as good as qwen2.5:14b though I dont expect it to keep up with more advanced pdfs

import os
import time
import json
import ollama
import pdfplumber
import re

PDF_FILE_PATH = "examplePDFs/Simple Mock Data.pdf"
#PDF_FILE_PATH = "examplePDFs/testpdf.pdf"
#LLM_MODEL="llama3.1:8b"
#LLM_MODEL="qwen2.5:14b"
LLM_MODEL="qwen2.5-coder:3b"


def extract_json_fragment(response_text):
    try:
        # Strip leading/trailing non-JSON text
        json_start = response_text.find("[")
        json_end = response_text.rfind("]")
        if json_start != -1 and json_end != -1:
            json_data = response_text[json_start:json_end + 1]
            return json.dumps(json.loads(json_data))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    print("Error: No valid JSON found in the response.")
    return None


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
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"seed": 1, "temperature":0}
    )

    return response

# List available models
#models = ollama.list()
#print("Available models:", models.models)

start_time = time.time()

extracted_data = extract_text_from_pdf(PDF_FILE_PATH)
print("Extracted Data")
print(extracted_data)
structured_data = process_text_with_llm(extracted_data)

print("Structured Data")
print(structured_data.message.content)

end_time = time.time()
elapsed_time = end_time - start_time

print(f"LLM processing time: {elapsed_time:.2f} seconds")

print("Output Json")
print(extract_json_fragment(structured_data.message.content))


