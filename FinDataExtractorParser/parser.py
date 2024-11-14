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

    file_name, file_extension = os.path.splitext(file.filename)
    unique_id = str(uuid.uuid4())
    unique_file_name = f"{file_name}({unique_id}){file_extension}"

    upload_folder = 'uploads'
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, unique_file_name)
    file.save(file_path)

    output_path = os.path.join(upload_folder, f"Output-{unique_id}.json")

    output_data = ["bees"]
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                output_data.append({"page_number": page.page_number, "text": text})

    with open(output_path, 'w') as f:
        json.dump(output_data, f)

    print(f"Data extracted to {output_path} in JSON format.")

    # Return success message with data
    return jsonify({"message": f"File {unique_file_name} uploaded successfully!", "data": output_data}), 200

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