import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pdfplumber
import json

app = Flask(__name__)
CORS(app)

@app.route('/parse', methods=['POST'])
def parse_PDF():
    # Check if the file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    output_data = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                output_data.append({"page_number": page.page_number, "text": text})

    # Print extracted data (optional)
    print(f"Data extracted from PDF: {output_data}")

    # Return the extracted data in JSON format as the response
    return jsonify({"message": "File uploaded and data extracted successfully!", "data": output_data}), 200

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