import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import time

from parse import fullParse

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

    # generate a unique filename and save file to temp directory (the llama functionality uses a filepath as of now)
    temp_filename = f"{uuid.uuid4()}.pdf"
    temp_filepath = os.path.join(UPLOAD_FOLDER, temp_filename)
    file.save(temp_filepath)

    print("saved temp file")

    try:
        # moved parsing to parse.py for easier local testing
        structured_data = fullParse(temp_filename)

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


# start_time = time.time()
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"LLM processing time: {elapsed_time:.2f} seconds")