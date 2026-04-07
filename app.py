from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import whisper
import os
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # Max 100MB file

# Create uploads folder if it doesn't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Load Whisper model once
print("Loading Whisper model...")
model = whisper.load_model("base")
print("Whisper model loaded successfully!")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    """Handle audio transcription requests"""
    try:
        # Check if file is in request
        if "file" not in request.files:
            return jsonify({"error": "No file part in request"}), 400
        
        file = request.files["file"]
        
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        
        # Validate file is audio
        allowed_extensions = {"mp3", "wav", "m4a", "ogg", "flac", "wma", "aac"}
        if not ("." in file.filename and file.filename.rsplit(".", 1)[1].lower() in allowed_extensions):
            return jsonify({"error": "Invalid file format. Allowed: MP3, WAV, M4A, OGG, FLAC"}), 400
        
        # Save uploaded file
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        
        print(f"Processing file: {file.filename}")
        
        # 👇 Language parameter frontend se aayega
        language = request.form.get("language", "en")  # default English
        
        # 👇 Transcribe using Whisper with language
        result = model.transcribe(filepath, language=language)
        transcription_text = result["text"]
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({"text": transcription_text}), 200
    
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    print("Starting Flask server...")
    print("Listening on http://127.0.0.1:5000")
    print("API: POST to /transcribe with audio file + language")
    app.run(debug=True, host="127.0.0.1", port=5000)
