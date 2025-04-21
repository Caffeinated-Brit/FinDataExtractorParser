import difflib
import json
import chardet  # pip install chardet
import configparser
import time
import os

import extractJSON
from configs import configLoader
from configs.ai_methods import ai_methods
from configs.parser_methods import parser_methods
from verification_parsing import verify_similar_outputs
from schemas.small_schema import FinancialData


def run_parse(parse_method, file_path):
    # Check that parsing method is valid
    try:
        if parse_method in parser_methods:
            extracted_text = parser_methods[parse_method](file_path)
            # check if pdf is image based, could implement more complex way of checking for images
            if extracted_text == "":
                print("No text found in pdf using \"" + parse_method + "\" method. Attempting OCR workaround.")
                extracted_text = parser_methods["pyTesseract"](file_path)
                if extracted_text == "":
                    print("No text found in pdf using OCR workaround. Exiting.")
                    return None

                print("Applied OCR workaround, continuing...")
        else:
            raise ValueError(f"Unknown parser method: {parse_method}")
    except FileNotFoundError as e:
        print("Pdf file not found, exiting.")
        raise e
    return extracted_text


# This is a good place to put any specific model config or other specific config at
def run_ai(ai_method, prompt, config, schema):
    if ai_method in ai_methods:
        print("Starting:", ai_method, " execution")
        # structured_data = ai_methods[ai_method](prompt)
        # display AI model used per the config.ini
        if "Ollama" in ai_method:
            print("Ollama Model used:", config["ollama_model"])
            print("Setting Ollama to have no cache")
            os.environ["OLLAMA_NO_CACHE"] = "1"  # this may or may not work I cannot tell, its fairly consitent with or without
            # structured_data = ai_methods[ai_method](prompt)
        if config["activeVerification"] == "True":
            print("Active Verification:", config["activeVerification"])

            structured_data = verify_similar_outputs(int(config["reruns"]), float(config["threshold"]), prompt, ai_method, schema)
        else:
            structured_data = ai_methods[ai_method](prompt, schema)
    else:
        raise ValueError(f"Unknown AI method: {ai_method}")
    return structured_data

def fullParse(input_filepath, schema):
    config = configLoader.load_config()
    selected_parser = config["parser"]
    selected_ai = config["ai"]

    start_time = time.time()

    # call chosen parsing method -----------------------------------
    extracted_text = run_parse(selected_parser, input_filepath)

    print("--- Parser time: %s seconds ---" % (time.time() - start_time))

    final_file_path = input_filepath.replace(".pdf", ".txt")

    if selected_parser != "linux_pdftotext":  # Writes to file manually for non-linux parsing methods, the linux parsing outputs its own txt file
        with open(final_file_path, "w") as file:
            file.write(extracted_text)
            print("Created output text at: " + final_file_path)

    print("\nDetecting file encoding...")

    # Detect encoding
    with open(final_file_path, "rb") as file:
        raw_data = file.read()
        detected_encoding = chardet.detect(raw_data)['encoding']

    print(f"Detected Encoding: {detected_encoding}")

    # Read file using the detected encoding (for input text files containing ASCII, UTF-8, or other encodings)
    with open(final_file_path, "r", encoding=detected_encoding, errors="replace") as file:
        extracted_text = file.read()

    # print("\nExtracted text:", "\n", extracted_text)

    # prompt = (
    #     f"The following text was extracted from a PDF named \"{input_filepath}\".\n"
    #     "Extract and categorize the data from the text. Return as JSON.\n"
    #     f"Text:\n{extracted_text}")

    prompt = config["prompt_template"].format(filepath=input_filepath, text=extracted_text)
    print("\nPrompt:", "\n", prompt)

    ai_time = time.time()

    # call chosen ai method ---------------------------------------------------
    structured_data = run_ai(selected_ai, prompt, config, schema)

    #print("\nAI output:", "\n", structured_data)
    print("--- AI time: %s seconds ---" % (time.time() - ai_time))

    try:
        if selected_ai != "gpt":
            # does not work with gpt, was made in a rush so it is poor
            structured_data = extractJSON.fix_truncated_json(structured_data)
        print("\nStructured data:", "\n", structured_data)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return None

    print("\nCreating JSON...")

    output_file_path = input_filepath.replace(".pdf", ".json")
    with open(output_file_path, "w", encoding="utf-8") as file:
        json.dump(structured_data, file, indent=4)
        print("Created output json at: " + output_file_path)

    print("--- Total time: %s seconds ---" % (time.time() - start_time))
    return structured_data


if __name__ == "__main__":
    # config = configLoader.load_config()
    # print(config)
    # selected_parser = config["parser"]
    # selected_ai = config["ai"]
    #
    # print(run_parse(selected_parser,"examplePDFs/fromCameron/2021_2_Statement_removed.pdf"))
    # print(run_ai(selected_ai, prompt))

    print(fullParse("C:/Users/lukas/Desktop/Capstone/FinDataExtractorParser/FinDataExtractorParser/examplePDFs/fromCameron/2021_2_Statement_removed.pdf", FinancialData.model_json_schema()))