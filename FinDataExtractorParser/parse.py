import json
import chardet # pip install chardet | GNU Lesser General Public License
# from AI import llama
import extractJSON
from AI import Ollama
# from PDFparsers import pyTesseract
from PDFparsers import pdfPlumber
# from PDFparsers.linux import linuxTest


def fullParse(inputfilepath):
    extracted_text = pdfPlumber.extract_text_from_pdf(inputfilepath) # WORKS
    # extracted_text = pyTesseract.extract_content(inputfilepath) # WORKS

    finalFilePath = inputfilepath.replace(".pdf", ".txt")
    print("filepath: ", finalFilePath)

    # extracted_text = linuxTest.linuxParse(inputfilepath)

    # NOTE if not using linux write to file manually here vvv
    with open(finalFilePath, "w") as file:
        file.write(extracted_text)

    print("\nDetecting file encoding...")

    # Detect encoding
    with open(finalFilePath, "rb") as file:
        raw_data = file.read()
        detected_encoding = chardet.detect(raw_data)['encoding']

    print(f"Detected Encoding: {detected_encoding}")

    # read file using the detected encoding (for input text files containting ASCII, UTF-8, or other encodings)
    with open(finalFilePath, "r", encoding=detected_encoding, errors="replace") as file:
        extracted_text = file.read()

    print("\nExtracted text:", "\n", extracted_text)

    prompt = (
        f"The following text was extracted from a PDF.\n"
        f"Ignore any terms and conditions, and only extract valuable financial data.\n"
        f"Categorize the extracted data into valid JSON format.\n"
        f"Ensure the JSON is fully valid and does not contain errors.\n"
        f"Return only the JSON array, with no extra text before or after.\n"
        # f"Make this text into a JSON. "
        f"Text:\n{extracted_text}\n"
    )

    print("\nPrompting AI...")

    # structured_data = gpt.extract_structured_data(prompt) # WORKS
    # structured_data = llama.process_text_with_llm(prompt) # WORKS, needs jsonify

    structured_data = Ollama.process_text_with_llm(prompt)  # USE THIS 1000000% OF THE TIME

    print("\nAI output:", "\n", structured_data)

    try:
        structured_data = extractJSON.fix_truncated_json(structured_data)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return None

        # Save JSON output
    print("\nCreating JSON...")
    with open(inputfilepath.replace(".pdf", ".json"), "w", encoding="utf-8") as file:
        json.dump(structured_data, file, indent=4)
        print("Created output.json")

    return structured_data


fullParse("examplePDFs/loan_statementCheckText.pdf")
# parses well
# 2021_2_Statement_removed

# AI hates these docs
# Principal_401k, schwab