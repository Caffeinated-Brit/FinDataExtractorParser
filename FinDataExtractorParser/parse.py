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
        "Ollama": Ollama.run_parallel_requests,
        "Ollama/Schema": Ollama.run_parallel_requests_with_schema,
        #"Vllm": Vllm.run_parallel_requests,
        # "llama": llama.process_text_with_llm,
        # "gpt": gpt.extract_structured_data
    }
    ai_time = time.time()
    # Check that AI method is valid
    if selected_ai in ai_methods:
        # Past this point elapsed_time and generated_tokens are not used they are only for benchmarking
        structured_data, elapsed_time, generated_tokens = generate_checked_text(5, 0.9, prompt, ai_methods)
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

# This runs the llm chosen multiple times to check that the output is consistent
def generate_checked_text(retries, threshold, prompt, ai_methods):
    outputs = ai_methods[selected_ai](retries, prompt)
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
    fullParse("C:/Users/lukas/Desktop/Capstone/FinDataExtractorParser/FinDataExtractorParser/examplePDFs/fromCameron/2021_2_Statement_removed.pdf")