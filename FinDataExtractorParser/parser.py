from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_PDF():
    # Get the JSON data from the request
    data = request.get_json()

    # Print JSON data to the console
    print(data)

    # Return a response
    return jsonify({"status": "success", "message": "Data printed to console"}), 200


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
    app.run(debug=True)