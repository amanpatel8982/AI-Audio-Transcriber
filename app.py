from flask import Flask, request, render_template
import whisper
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Load Whisper model once
model = whisper.load_model("base")

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        audio = request.files["file"]
        if audio.filename == "":
            return "No selected file"

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], audio.filename)
        audio.save(filepath)

        result = model.transcribe(filepath)
        return render_template("index.html", transcription=result["text"])

    return render_template("index.html", transcription=None)

if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(debug=True)
