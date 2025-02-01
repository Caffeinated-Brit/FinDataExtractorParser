import json
import chardet # pip install chardet | GNU Lesser General Public License
# from AI import llama
from AI import Ollama


def fix_truncated_json(ai_output):
    try:
        return json.loads(ai_output)  # Try parsing normally
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}\nAttempting auto-fix...")

        # Attempt to auto-fix by trimming at the last valid closing bracket
        last_curly = ai_output.rfind("}")
        last_square = ai_output.rfind("]")

        last_valid = max(last_curly, last_square)  # Find last valid closing bracket
        if last_valid == -1:
            print("no valid json structure found")
            return None  # No valid JSON structure found

        fixed_json = ai_output[:last_valid+1]  # Trim to last valid bracket

        try:
            return json.loads(fixed_json)  # Retry parsing the fixed JSON
        except json.JSONDecodeError:
            print("still broken")
            return None  # Still broken

def process_text_file(filepath):
    # extracted_text = pdfPlumber.extract_text_from_pdf(temp_filepath) # WORKS
    # extracted_text = pyTesseract.extract_content(temp_filepath) # WORKS

    print("\nDetecting file encoding...")
    
    # Detect encoding
    with open(filepath, "rb") as file:
        raw_data = file.read()
        detected_encoding = chardet.detect(raw_data)['encoding']
    
    print(f"Detected Encoding: {detected_encoding}")

    # Read the file using the detected encoding
    with open(filepath, "r", encoding=detected_encoding, errors="replace") as file:
        extracted_text = file.read()

    print("\nExtracted text:", "\n", extracted_text)

    # Process with AI
    prompt = (
    f"The following text was extracted from a PDF. Format it into categorized JSON.\n"
    f"Ensure the JSON is fully valid and does not contain errors.\n"
    f"Return only the JSON array, with no extra text before or after.\n"
    f"Text:\n{extracted_text}\n"
    )

    print("\nPrompting AI...")

    # structured_data = gpt.extract_structured_data(prompt) # WORKS
    # structured_data = llama.process_text_with_llm(prompt) # WORKS, needs jsonify
    structured_data = Ollama.process_text_with_llm(prompt)
    # structured_data = llama.process_text_with_llm(prompt)

    print("\nAI output:", "\n", structured_data)

    try:
        structured_data = fix_truncated_json(structured_data)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return None  

    # Save JSON output
    print("\nCreating JSON...")
    with open("FinDataExtractorParser/output.json", "w", encoding="utf-8") as file:
        json.dump(structured_data, file, indent=4)
        print("Created output.json")

    return structured_data

process_text_file("FinDataExtractorParser/PDFparsers/linux/output.txt")