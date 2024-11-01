import uuid

from flask import Flask, request, jsonify
import os
import tabula
import json
app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_PDF():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400


    file_name, file_extension = os.path.splitext(file.filename)

    unique_id = str(uuid.uuid4())

    unique_file_name = str(file_name + "(" + unique_id + ")" +file_extension)


    upload_folder = 'uploads'
    os.makedirs(upload_folder, exist_ok=True)  # Create the directory if it doesn't exist
    file_path = os.path.join(upload_folder, unique_file_name)

    # Save the uploaded file to the specified path
    file.save(file_path)

    file_path = "./uploads/" + unique_file_name
    output_path = "./uploads/" + "Output" + "-" + unique_file_name

    tabula.convert_into(file_path, output_path, output_format="json", pages="all")

    print(f"Data extracted to {output_path} in JSON format.")

    with open(output_path, 'r') as output_file:
        output_data = json.load(output_file)  # Load the JSON data

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
    app.run(port=5000, debug=True)