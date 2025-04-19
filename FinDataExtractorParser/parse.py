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

def run_ai(ai_method, prompt, config):
    if ai_method in ai_methods:
        print("Starting:", ai_method, " execution")
        # structured_data = ai_methods[ai_method](prompt)
        # display AI model used per the config.ini
        if "Ollama" in ai_method:
            print("Ollama Model used:", config["ollama_model"])
            print("Setting Ollama to have no cache")
            os.environ["OLLAMA_NO_CACHE"] = "1"  # this may or may not work I cannot tell, its fairly consitent with or without
            # structured_data = ai_methods[ai_method](prompt)
        # structured_data, elapsed_time, generated_tokens = ai_methods[ai_method](prompt)
    else:
        raise ValueError(f"Unknown AI method: {ai_method}")

    structured_data, elapsed_time, generated_tokens = verify_similar_outputs(3, 0.9, prompt, ai_method)
    return structured_data
    #return ai_methods[ai_method](prompt)

def fullParse(input_filepath):
    config = configLoader.load_config()
    selected_parser = config["parser"]
    selected_ai = config["ai"]
    selected_schema = config["schema"]

    start_time = time.time()

    # call chosen parsing method -----------------------------------
    extracted_text = run_parse(selected_parser, input_filepath)

    print("--- Parser time: %s seconds ---" % (time.time() - start_time))

    final_file_path = input_filepath.replace(".pdf", ".txt")

    if selected_parser != "linux_pdftotext":  # Writes to file manually for non-linux parsing methods, the linux parsing outputs its own txt file
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
        f"Text:\n{extracted_text}")

    ai_time = time.time()

    # call chosen ai method ---------------------------------------------------
    structured_data = run_ai(selected_ai, prompt, config)

    #print("\nAI output:", "\n", structured_data)
    print("--- AI time: %s seconds ---" % (time.time() - ai_time))

    try:
        # does not work with gpt, also not really needed anymore, also was made in a rush so it is poor, commenting out for now
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

#This will run the selected ai multiple times and output the most similar to the others
def verify_similar_outputs(reruns, threshold, prompt, selected_ai):
    outputs = ai_methods[selected_ai](reruns, prompt)
    print("Checking similarity ratio of the following outputs.\n")

    num_outputs = len(outputs)
    total_similarity = [0.0] * num_outputs
    comparison_counts = [0] * num_outputs

    # Compare each output against all others
    for i in range(num_outputs):
        norm_i = normalize_json_string(outputs[i][0])
        for j in range(num_outputs):
            if i == j:
                continue
            norm_j = normalize_json_string(outputs[j][0])
            similarity = difflib.SequenceMatcher(None, norm_i, norm_j).ratio()
            print(f"Similarity between {i} and {j}: {similarity:.2f}")

            total_similarity[i] += similarity
            comparison_counts[i] += 1

    average_similarity = [
        total / count if count > 0 else 0.0
        for total, count in zip(total_similarity, comparison_counts)
    ]

    print()
    for i, avg in enumerate(average_similarity):
        print(f"Average similarity for output {i}: {avg:.2f}")

    highest_similarity = max(average_similarity)

    # Pick the first output with the highest average similarity
    best_index = average_similarity.index(highest_similarity)

    if average_similarity[best_index] > threshold:
        print(f"\nReturning output {best_index} (avg similarity: {average_similarity[best_index]:.2f})")
        return outputs[best_index]

    print("\nNo sufficiently similar outputs found, defaulting to first.")
    return outputs[0]

def normalize_json_string(text):
    try:
        if text.startswith("```json"):
            lines = text.strip().splitlines()
            text = "\n".join(lines[1:-1])

        parsed = json.loads(text)
        return json.dumps(parsed, sort_keys=True)
    except Exception as e:
        print("⚠️ Could not normalize output:", e)
        return text



if __name__ == "__main__":
    # config = configLoader.load_config()
    # print(config)
    # selected_parser = config["parser"]
    # selected_ai = config["ai"]
    #
    # print(run_parse(selected_parser,"examplePDFs/fromCameron/2021_2_Statement_removed.pdf"))
    # print(run_ai(selected_ai, prompt))

    print(fullParse("C:/Users/lukas/Desktop/Capstone/FinDataExtractorParser/FinDataExtractorParser/examplePDFs/fromCameron/2021_2_Statement_removed.pdf"))