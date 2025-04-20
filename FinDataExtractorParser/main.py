import uuid
import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from parse import fullParse

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads/" # Temporary folder for uploaded files, possibly the database in the future
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/parse', methods=['POST'])
def parse_pdf():

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # accept json schema for Ollama as a file from the backend
    if 'schema' in request.files:
        schema = request.files.get('schema')

        # Read and decode schema file
        schema.seek(0)  # in case it was read earlier
        schema_content = schema.read().decode('utf-8')

        # Check if the schema file is empty (after trimming whitespace)
        if not schema_content.strip():
            print("Schema file is empty!")
            schema_content = None
        else:
            print(f"File: {file.filename}, Content-Type: {file.content_type}")
            print(f"Schema: {schema.filename}, Content-Type: {schema.content_type}")
            # print(schema_content)
    else:
        schema_content = None

    # Generate a unique filename and save file to temp directory (the llama functionality uses a filepath as of now)
    temp_filepath = f"{UPLOAD_FOLDER}{file.filename}"
    file.save(temp_filepath)

    print("Saved temp file")

    try:
        # Call fullParse() in parse.py
        structured_data = fullParse(temp_filepath, schema_content)
        return jsonify({"message": "File uploaded and processed successfully!", "data": structured_data}), 200
    except Exception as e:
        print("Exception in fullParse:", str(e))  # Debugging line
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
    app.run(host='0.0.0.0', port=5000)