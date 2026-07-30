import boto3
from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
import os
app = Flask(__name__)
BUCKET_NAME = "docvault-uploads-mahi-2026"
REGION = "ap-south-2"
s3 = boto3.client(
    "s3",
    region_name=REGION
)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"message": "No file selected"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No file selected"}), 400
    try:
        s3.upload_fileobj(
            file,
            BUCKET_NAME,
            f"incoming/{file.filename}"
        )
        return jsonify({
            "message": "Uploaded successfully!"
        })
    except Exception as e:
        return jsonify({"message": str(e)}), 500
@app.route("/files")
def files():
    try:
        response = s3.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix="processed/"
        )
        file_list = []
        if "Contents" in response:
            for obj in response["Contents"]:
                key = obj["Key"]
                if key.endswith("/"):
                    continue
                file_list.append({
                    "name": key,
                    "size": round(obj["Size"] / 1024, 2)
                })
        return jsonify(file_list)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
@app.route("/download/<path:filename>")
def download(filename):
    file_stream = BytesIO()
    s3.download_fileobj(
        BUCKET_NAME,
        filename,
        file_stream
    )
    file_stream.seek(0)
    return send_file(
        file_stream,
        as_attachment=True,
        download_name=os.path.basename(filename)
    )
@app.route("/delete/<path:filename>", methods=["DELETE"])
def delete(filename):
    s3.delete_object(
        Bucket=BUCKET_NAME,
        Key=filename
    )
    return jsonify({
        "message": "Deleted Successfully"
    })
if __name__ == "__main__":
    app.run(debug=True)