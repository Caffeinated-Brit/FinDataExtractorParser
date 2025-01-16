import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import time
# import other folders 
from AI import gpt, llama
from PDFparsers import pytesseract, pdfplumber

FILE_PATH = "FinDataExtractorParser/examplePDFs/Simple Mock Data.pdf"

app = Flask(__name__)
CORS(app)

# Temporary folder for uploaded files, possibly the database in the future
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/parse', methods=['POST'])
def parse_PDF():
    # Check if the file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # generate a unique filename and save file to temperarily (the llama functionality uses a filepath as of now)
    temp_filename = f"{uuid.uuid4()}.pdf"
    temp_filepath = os.path.join(UPLOAD_FOLDER, temp_filename)
    file.save(temp_filepath)

    try:
        extracted_text = pdfplumber.extract_text_from_pdf(FILE_PATH) # WORKS
        # extracted_text = pytesseract.extract_content(FILE_PATH) # WORKS

        prompt = (
            f"Follow the listed steps to analyze the following text and extract information. \n"
            f"Step 1: identify the key pieces of information in the text. "
            f"Do not print any text for this step. \n"
            f"Step 2: extract the information for each key. "
            f"Do not print any text for this step. \n"
            f"Step 3: format the extracted information into a JSON array. \n"
            f"Text for you to analyze:\n{extracted_text} \n"
            f"Return only your final answer in a JSON array.\n")

        # prompt = "give me 3 space facts"

        # structured_data = Gpt.extract_structured_data(prompt) # WORKS
        structured_data = llama.process_text_with_llm(prompt) # WORKS, needs jsonify
        # structured_data = Ollama.process_text_with_llm(prompt)

        return jsonify({"message": "File uploaded and processed successfully!", "data": structured_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # delete temporary file
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

@app.route('/sample', methods=['POST'])
def print_json():
    # Get the JSON data from the request
    data = request.get_json()
    # Print JSON data to the console
    print("Received JSON data:", data)
    # Return a response
    return jsonify({"status": "success", "message": "Data printed to console"}), 200

@app.route('/sample', methods=['GET'])
def get_json():
    # Return a simple message for the GET request
    return jsonify({"status": "success", "message": "GET request received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



# NOTE removes not json text from output VVVVVVV
# def extract_json_fragment(response_text):
#     try:
#         # Strip leading/trailing non-JSON text
#         json_start = response_text.find("[")
#         json_end = response_text.rfind("]")
#         if json_start != -1 and json_end != -1:
#             json_data = response_text[json_start:json_end + 1]
#             return json.dumps(json.loads(json_data))
#     except json.JSONDecodeError as e:
#         print(f"Error parsing JSON: {e}")
#     print("Error: No valid JSON found in the response.")
#     return None


# start_time = time.time()
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"LLM processing time: {elapsed_time:.2f} seconds")