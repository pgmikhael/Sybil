from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pydicom
import numpy as np
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "dcm"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def process_image(file_path):
    # Dummy function to simulate prediction and overlay generation
    # Replace with actual model prediction and overlay logic
    if file_path.endswith(".dcm"):
        ds = pydicom.dcmread(file_path)
        image = ds.pixel_array
    else:
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    # Dummy prediction and overlay
    prediction = "dummy_prediction"
    overlay = np.zeros_like(image)

    return prediction, overlay


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        prediction, overlay = process_image(file_path)

        # Save overlay image
        overlay_path = os.path.join(app.config["UPLOAD_FOLDER"], "overlay_" + filename)
        cv2.imwrite(overlay_path, overlay)

        return jsonify({"prediction": prediction, "overlay_path": overlay_path}), 200

    return jsonify({"error": "File type not allowed"}), 400


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
