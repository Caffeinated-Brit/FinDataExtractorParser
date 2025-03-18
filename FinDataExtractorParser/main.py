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

    # Generate a unique filename and save file to temp directory (the llama functionality uses a filepath as of now)
    temp_filepath = f"{UPLOAD_FOLDER}{file.filename}"
    file.save(temp_filepath)

    print("Saved temp file")

    # Call fullParse() in parse.py
    try:
        structured_data = fullParse(temp_filepath)
        return jsonify({"message": "File uploaded and processed successfully!", "data": structured_data}), 200
    except Exception as e:
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