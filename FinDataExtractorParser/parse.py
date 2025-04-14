import json
import chardet  # pip install chardet
import configparser
import time
import difflib
from concurrent.futures import ThreadPoolExecutor

import extractJSON
from AI import Vllm
from FinDataExtractorParser.AI import Ollama
# gpt
# from AI import llama # Phasing out llama bc it's too slow and lowkey trash
from PDFparsers import pdfPlumber, pyTesseract, linuxTest

# Load configuration
config = configparser.ConfigParser()
config.read("config.ini")
selected_parser = config.get("Parser", "method", fallback="pdfPlumber")
selected_ai = config.get("AI", "method", fallback="Ollama")

def fullParse(input_filepath):
    start_time = time.time()
    # Pick parsing method based on config
    parser_methods = {
        "pdfPlumber": pdfPlumber.extract_text_from_pdf,
        "pyTesseract": pyTesseract.extract_content,
        "linuxTest": linuxTest.linuxParse
    }

    # Check that parsing method is valid
    if selected_parser in parser_methods:
        extracted_text = parser_methods[selected_parser](input_filepath)
        # check if pdf is image based, could implement more complex way of checking with
        if extracted_text == "":
            print("No text found in pdf using \"" + selected_parser + "\" method. Attempting OCR workaround.")
            extracted_text = parser_methods["pyTesseract"](input_filepath)
            if extracted_text == "":
                print("No text found in pdf using OCR workaround. Exiting.")
                return None

            print("Applied OCR workaround, continuing...")
    else:
        raise ValueError(f"Unknown parser method: {selected_parser}")

    print("--- Parser time: %s seconds ---" % (time.time() - start_time))

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
        f"The following text was extracted from a PDF named \"{input_filepath}\".\n"
        "Extract and categorize the data from the text. Return as JSON.\n"
        # "Ignore any terms and conditions, and only extract valuable financial data.\n"
        # "Categorize the extracted data into valid JSON format.\n"
        # "Ensure the JSON is fully valid and does not contain errors.\n"
        # "Return only the JSON array, with no extra text before or after.\n"
        f"Text:\n{extracted_text}")

    # Pick AI method based on config
    ai_methods = {
        "Ollama": Ollama.process_text_with_llm,
        "Ollama/Schema": Ollama.process_text_with_llm_and_schema,
        "vllm": Vllm.run_parallel_requests,
        # "llama": llama.process_text_with_llm,
        # "gpt": gpt.extract_structured_data
    }

    ai_time = time.time()
    # Check that AI method is valid
    if selected_ai in ai_methods:
        #structured_data = generate_checked_text(prompt)
        #structured_data = ai_methods[selected_ai](prompt)
        #structured_data, elapsed_time, generated_tokens = ai_methods[selected_ai](prompt)
        structured_data, elapsed_time, generated_tokens = generate_checked_text(10, 0.5, prompt, ai_methods)
    else:
        raise ValueError(f"Unknown AI method: {selected_ai}")

    print("\nAI output:", "\n", structured_data)
    print("--- AI time: %s seconds ---" % (time.time() - ai_time))

    try:
        structured_data = extractJSON.fix_truncated_json(structured_data)
        print("\nStructured data:", "\n", structured_data)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return None

    print("\nCreating JSON...")

    output_file_path = input_filepath.replace(".pdf", ".json")
    with open(output_file_path, "w", encoding="utf-8") as file:
        json.dump(structured_data, file, indent=4)
        print("Created output.json")

    print("--- Total time: %s seconds ---" % (time.time() - start_time))
    return structured_data


def generate_checked_text(retries, threshold, prompt, ai_methods):
    output = ai_methods[selected_ai](retries, prompt)

    print("Checking similarity ratio of the following outputs.")
    for i in range(len(output)):
        for j in range(i + 1, len(output)):
            norm_i = normalize_json_string(output[i][0])
            norm_j = normalize_json_string(output[j][0])

            ratio = difflib.SequenceMatcher(None, norm_i, norm_j).ratio()

            print(f"Matched outputs with similarity {ratio:.2f}")
            if ratio > threshold:
                return output[i]

    print("No sufficiently similar outputs found, defaulting to first.")
    return output[0]

def normalize_json_string(text):
    try:
        # Remove Markdown-style ```json ... ``` if present
        if text.startswith("```json"):
            lines = text.strip().splitlines()
            # Drop first (```json) and last (```)
            text = "\n".join(lines[1:-1])

        parsed = json.loads(text)
        print(parsed)
        return json.dumps(parsed, sort_keys=True)
    except Exception as e:
        print("⚠️ Could not normalize output:", e)
        return text

if __name__ == "__main__":
    fullParse("C:/Users/lukas/Desktop/Capstone/FinDataExtractorParser/FinDataExtractorParser/examplePDFs/fromCameron/2021_2_Statement_removed.pdf")