from flask import Flask, request, jsonify, send_from_directory
import os
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = "media/"
DATA_FILE = "media/resources.xlsx"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load existing data or create a new Excel file
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Name", "Author", "Year", "Type", "URL"])
    df.to_excel(DATA_FILE, index=False)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    df = pd.read_excel(DATA_FILE)
    new_entry = {"Name": file.filename, "Author": "Unknown", "Year": "Unknown", "Type": "File", "URL": file_path}
    df = df.append(new_entry, ignore_index=True)
    df.to_excel(DATA_FILE, index=False)

    return jsonify({"message": "File uploaded successfully"}), 200

@app.route("/add_url", methods=["POST"])
def add_url():
    data = request.json
    df = pd.read_excel(DATA_FILE)
    new_entry = {"Name": data["name"], "Author": data["author"], "Year": data["year"], "Type": data["type"], "URL": data["url"]}
    df = df.append(new_entry, ignore_index=True)
    df.to_excel(DATA_FILE, index=False)

    return jsonify({"message": "URL added successfully"}), 200

@app.route("/get_resources", methods=["GET"])
def get_resources():
    df = pd.read_excel(DATA_FILE)
    return jsonify(df.to_dict(orient="records"))

@app.route("/literature/<path:filename>")
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
