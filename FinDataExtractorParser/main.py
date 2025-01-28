import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import time
# import other folders 
from AI import gpt #, llama, Ollama
# from PDFparsers import pyTesseract, pdfPlumber
from PDFparsers import pdfPlumber

app = Flask(__name__)
CORS(app)

# Temporary folder for uploaded files, possibly the database in the future
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_json_fragment(response_object):
    try:
        # Extract the content if it exists
        content_text = getattr(response_object, 'content', None)
        if content_text:
            # Extract JSON array from content
            json_start = content_text.find("[")
            json_end = content_text.rfind("]")
            if json_start != -1 and json_end != -1:
                return json.dumps(json.loads(content_text[json_start:json_end + 1]))  # Validate and return JSON
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    # print("Error: No valid JSON found in the response.")
    return None

@app.route('/parse', methods=['POST'])
def parse_PDF():
    # print("DEBUG: /parse endpoint hit, starting parse_PDF function")
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Generate a unique filename and save file to temp directory (the llama functionality uses a filepath as of now)
    temp_filename = f"{uuid.uuid4()}.pdf"
    temp_filepath = os.path.join(UPLOAD_FOLDER, temp_filename)
    file.save(temp_filepath)

    try:
        # print("DEBUG: Starting text extraction")

        extracted_text = pdfPlumber.extract_text_from_pdf(temp_filepath)
        # extracted_text = pyTesseract.extract_content(temp_filepath)

        # print(f"DEBUG: Extracted text: {extracted_text}")
        # print("DEBUG: Constructing GPT prompt")


        prompt = (
            f"Follow the listed steps to analyze the following text and extract information. \n"
            f"Step 1: identify the key pieces of information in the text. "
            f"Do not print any text for this step. \n"
            f"Step 2: extract the information for each key. "
            f"Do not print any text for this step. \n"
            f"Step 3: format the extracted information into a JSON array. \n"
            f"Text for you to analyze:\n{extracted_text} \n"
            f"Return only your final answer in a JSON array.\n")

        # print("DEBUG: Sending prompt to LLM for structured data extraction")

        structured_data = gpt.extract_structured_data(prompt)
        # structured_data = llama.process_text_with_llm(prompt)
        # structured_data = Ollama.process_text_with_llm(prompt)

        # print(f"DEBUG: Received structured data: {structured_data}")

        # print("DEBUG: Cleaning up LLM response to extract JSON fragment")
        json_fragment = extract_json_fragment(structured_data)
        if not json_fragment:
            raise ValueError("Failed to extract valid JSON from LLM response.")

        # print(f"DEBUG: Returning final structured JSON data: {json_fragment}")
        return jsonify({"message": "File uploaded and processed successfully!", "data": json.loads(json_fragment)}), 200

    except Exception as e:
        # print(f"ERROR: Exception occurred: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        # print("DEBUG: Cleaning up the temporary file")
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

@app.route('/sample', methods=['POST'])
def print_json():
    # print("DEBUG: /sample POST endpoint hit, processing JSON data")
    # Get the JSON data from the request
    data = request.get_json()
    # print(f"DEBUG: Received JSON data: {data}")
    return jsonify({"status": "success", "message": "Data printed to console"}), 200

@app.route('/sample', methods=['GET'])

def get_json():
    # print("DEBUG: /sample GET endpoint hit, returning static message")
    # Return a simple message for the GET request
    return jsonify({"status": "success", "message": "GET request received"}), 200

if __name__ == '__main__':
    # print("DEBUG: Starting Flask server on host 0.0.0.0 and port 5000")
    app.run(host='0.0.0.0', port=5000)