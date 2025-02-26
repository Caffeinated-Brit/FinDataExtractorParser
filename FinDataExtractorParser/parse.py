import json
import chardet  # pip install chardet | GNU Lesser General Public License
import configparser

import extractJSON
from AI import Ollama, LmDeploy
# gpt
# from AI import llama # Phasing out llama bc it's too slow and lowkey trash
from PDFparsers import pdfPlumber

# Load configuration
config = configparser.ConfigParser()
config.read("config.ini")
selected_parser = config.get("Parser", "method", fallback="pdfPlumber")
selected_ai = config.get("AI", "method", fallback="Ollama")

def fullParse(input_filepath):  # New parsing method allowing for easier local testing
    # Pick parsing method based on config
    parser_methods = {
        "pdfPlumber": pdfPlumber.extract_text_from_pdf,
        #"pyTesseract": pyTesseract.extract_content,
        #"linuxTest": linuxTest.linuxParse
    }

    # Check that parsing method is valid
    if selected_parser in parser_methods:
        extracted_text = parser_methods[selected_parser](input_filepath)
    else:
        raise ValueError(f"Unknown parser method: {selected_parser}")

    final_file_path = input_filepath.replace(".pdf", ".txt")

    if selected_parser != "linuxTest":  # Writes to file manually for non-linux parsing methods
        with open(final_file_path, "w") as file:
            file.write(extracted_text)

    print("\nDetecting file encoding...")

    # Detect encoding
    with open(final_file_path, "rb") as file:
        raw_data = file.read()
        detected_encoding = chardet.detect(raw_data)['encoding']

    print(f"Detected Encoding: {detected_encoding}")

    # Read file using the detected encoding (for input text files containing ASCII, UTF-8, or other encodings)
    with open(final_file_path, "r", encoding=detected_encoding, errors="replace") as file:
        extracted_text = file.read()

    print("\nExtracted text:", "\n", extracted_text)

    prompt = (
        "The following text was extracted from a PDF.\n"
        "Ignore any terms and conditions, and only extract valuable financial data.\n"
        "Categorize the extracted data into valid JSON format.\n"
        "Ensure the JSON is fully valid and does not contain errors.\n"
        "Return only the JSON array, with no extra text before or after.\n"
        f"Text:\n{extracted_text}\n"
    )

    print("\nPrompting AI...")

    # Pick AI method based on config
    ai_methods = {
        "Ollama": Ollama.process_text_with_llm,
        "LmDeploy": LmDeploy.process_text_with_llm,
        # "llama": llama.process_text_with_llm,
        # "gpt": gpt.extract_structured_data
    }

    # Check that AI method is valid
    if selected_ai in ai_methods:
        structured_data = ai_methods[selected_ai](prompt)
    else:
        raise ValueError(f"Unknown AI method: {selected_ai}")

    print("\nAI output:", "\n", structured_data)

    try:
        structured_data = extractJSON.fix_truncated_json(structured_data)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return None

    print("\nCreating JSON...")

    output_file_path = input_filepath.replace(".pdf", ".json")
    with open(output_file_path, "w", encoding="utf-8") as file:
        json.dump(structured_data, file, indent=4)
        print("Created output.json")

    return structured_data

if __name__ == "__main__":
    fullParse("examplePDFs/fromCameron/2021_2_Statement_removed.pdf")

# parses well
# 2021_2_Statement_removed

# AI hates these docs
# Principal_401k, schwab