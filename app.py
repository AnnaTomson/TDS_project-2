from flask import Flask, request, jsonify, abort
import os
import tempfile
import base64
from typing import Dict, Any, Optional
from pathlib import Path
from agents.task_executor import TaskExecutor

app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = {'txt', 'csv', 'json', 'xlsx', 'xls', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize the AI agent
executor = TaskExecutor()

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/api/", methods=["POST"])
def analyze():
    # Check if the post request has the file part
    if 'questions.txt' not in request.files:
        return jsonify({"error": "No questions.txt file provided"}), 400
    
    # Save uploaded files
    files = {}
    for file_key, file in request.files.items():
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            files[filename] = filepath
    
    # Read questions
    questions_path = files.get('questions.txt')
    if not questions_path:
        return jsonify({"error": "questions.txt not found in uploaded files"}), 400
    
    try:
        with open(questions_path, 'r') as f:
            task = f.read()
        
        # Process the task with the executor, passing all uploaded files
        result = executor.run(task, file_paths=list(files.values()))
        
        # Clean up uploaded files
        for filepath in files.values():
            try:
                os.remove(filepath)
            except:
                pass
                
        return jsonify(result)
        
    except Exception as e:
        # Clean up in case of error
        for filepath in files.values():
            try:
                os.remove(filepath)
            except:
                pass
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
