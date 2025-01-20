import uuid
import os
import json
import time
import shutil
from flask import Flask, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
from sybil.predict import predict

# Cấu hình ứng dụng Flask
app = Flask(__name__)

# Cấu hình thư mục tải lên và lưu trữ kết quả
UPLOAD_FOLDER = "uploads"
RESULTS_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"dcm", "png", "jpg", "jpeg"}

app.config.update(UPLOAD_FOLDER=UPLOAD_FOLDER, RESULTS_FOLDER=RESULTS_FOLDER)


def allowed_file(filename):
    """Kiểm tra tệp có định dạng phù hợp không"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def cleanup_old_results(expiry_time=3600):
    """Xóa thư mục cũ sau khoảng thời gian nhất định (3600 giây = 1 giờ)"""
    current_time = time.time()
    for folder in os.listdir(app.config["RESULTS_FOLDER"]):
        folder_path = os.path.join(app.config["RESULTS_FOLDER"], folder)
        if (
            os.path.isdir(folder_path)
            and (current_time - os.path.getmtime(folder_path)) > expiry_time
        ):
            shutil.rmtree(folder_path)
            print(f"Deleted old result folder: {folder_path}")


# Chạy dọn dẹp mỗi khi ứng dụng khởi động
cleanup_old_results()


@app.route("/api_predict", methods=["POST"])
def api_predict():
    """API nhận ảnh, chạy mô hình và trả về dự đoán và overlayed_images"""

    print("API predict called")

    files = request.files.getlist("file")  # Nhận tất cả các tệp tải lên
    if not files or all(file.filename == "" for file in files):
        return jsonify({"error": "No selected files"}), 400

    uploaded_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            uploaded_files.append(file_path)
            print("Uploaded file:", filename)
        else:
            return (
                jsonify({"error": "Invalid file type. Only DICOM or PNG allowed."}),
                400,
            )

    if not uploaded_files:
        return jsonify({"error": "No valid files uploaded"}), 400

    # Tạo UUID cho mỗi yêu cầu dự đoán
    session_id = str(uuid.uuid4())
    output_dir = os.path.join(app.config["RESULTS_FOLDER"], session_id)
    os.makedirs(output_dir, exist_ok=True)

    print(f"Session ID: {session_id}, Output directory: {output_dir}")

    # Chạy dự đoán với tất cả các file đã upload
    pred_dict, overlayed_images = predict(
        app.config["UPLOAD_FOLDER"], output_dir, write_attention_images=True
    )

    # Truy cập thư mục serie_0 để lấy ảnh overlay - chỉ có 1 serie trong trường hợp này
    overlay_dir = os.path.join(output_dir, "serie_0")
    overlay_files = [f for f in os.listdir(overlay_dir) if f.endswith(".png")]

    if not overlay_files:
        print("No overlay images found.")
    else:
        print("Overlay images found:", overlay_files)

    # Tạo danh sách các URL tải và xem trước ảnh
    base_url = request.host_url.rstrip("/")
    response = {
        "session_id": session_id,
        "predictions": pred_dict["predictions"],
        "overlay_images": {
            "download_links": [
                f"{base_url}/download/{session_id}/{img}" for img in overlay_files
            ],
            "preview_links": [
                f"{base_url}/preview/{session_id}/{img}" for img in overlay_files
            ],
            "gif_download": f"{base_url}/download_gif/{session_id}",
        },
        "message": "Prediction successful. Download overlay images using the provided links.",
    }

    return jsonify(response)


@app.route("/download/<session_id>/<filename>", methods=["GET"])
def download_file(session_id, filename):
    """API để tải xuống ảnh overlay theo session ID"""
    file_path = os.path.join(
        app.config["RESULTS_FOLDER"], session_id, "serie_0", filename
    )
    return (
        send_file(file_path, as_attachment=True)
        if os.path.exists(file_path)
        else jsonify({"error": "File not found"})
    ), 404


@app.route("/preview/<session_id>/<filename>", methods=["GET"])
def preview_file(session_id, filename):
    """API để xem trước ảnh overlay trực tiếp trên trình duyệt"""
    overlay_dir = os.path.join(app.config["RESULTS_FOLDER"], session_id, "serie_0")
    return (
        send_from_directory(overlay_dir, filename)
        if os.path.exists(os.path.join(overlay_dir, filename))
        else jsonify({"error": "File not found"})
    ), 404


@app.route("/download_gif/<session_id>", methods=["GET"])
def download_gif(session_id):
    """API để tải xuống file GIF của ảnh overlay"""
    gif_filename = "serie_0.gif"
    gif_path = os.path.join(
        app.config["RESULTS_FOLDER"], session_id, "serie_0", gif_filename
    )

    print(f"Checking GIF path: {gif_path}")  # Debugging

    if os.path.exists(gif_path):
        return send_file(gif_path, as_attachment=True)

    return jsonify({"error": "GIF file not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
