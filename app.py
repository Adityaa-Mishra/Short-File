from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Frontend file

@app.route("/convert", methods=["POST", "OPTIONS"], strict_slashes=False)
def convert_file():
    if request.method == 'OPTIONS':
        return ('', 200)

    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]
    target = request.form.get("target")

    if not file or file.filename == "":
        return "No selected file", 400

    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)

    try:
        img = Image.open(file.stream)
        img_io = io.BytesIO()

        if target.lower() in ["png", "jpg", "jpeg"]:
            img.save(img_io, format=target.upper())
        elif target.lower() == "pdf":
            img.save(img_io, format="PDF")
        else:
            return "Unsupported conversion type", 400

        img_io.seek(0)
        output_filename = f"{name}_converted.{target}"
        return send_file(img_io, as_attachment=True, download_name=output_filename)

    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
