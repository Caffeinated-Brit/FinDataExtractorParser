import uuid
import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from parse import fullParse

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads/" # Temporary folder for uploaded files, possibly the database in the future
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
def parse_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Generate a unique filename and save file to temp directory (the llama functionality uses a filepath as of now)
    temp_filepath = f"{UPLOAD_FOLDER}{uuid.uuid4()}.pdf"
    file.save(temp_filepath)

    print("Saved temp file")

    # Call fullParse() in parse.py
    try:
        structured_data = fullParse(temp_filepath)
        return jsonify({"message": "File uploaded and processed successfully!", "data": structured_data}), 200
    except Exception as e:
        # print(f"ERROR: Exception occurred: {e}")
        return jsonify({"error": str(e)}), 500
    # finally:
        # if os.path.exists(temp_filepath):
        #     os.remove(temp_filepath) # Delete temp file

@app.route('/sample', methods=['POST'])
def print_json():
    data = request.get_json()
    print("Received JSON data:", data)
    return jsonify({"status": "success", "message": "Data printed to console"}), 200

@app.route('/sample', methods=['GET'])

def get_json():
    return jsonify({"status": "success", "message": "GET request received"}), 200

if __name__ == '__main__':
    # print("DEBUG: Starting Flask server on host 0.0.0.0 and port 5000")
    app.run(host='0.0.0.0', port=5000)