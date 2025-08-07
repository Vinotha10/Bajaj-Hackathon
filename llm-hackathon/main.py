from flask import Flask, request, jsonify
from qa_engine import answer_question

import os
import requests

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Step 1: Upload file
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['document']

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        return jsonify({
            "message": "File uploaded successfully.",
            "file_path": file_path,
            "note": "Now send your question to /ask endpoint with this file path."
        })

    return "No file uploaded", 400

# Step 2: Ask a question
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    file_path = data.get("file_path")
    question = data.get("question")

    if not file_path or not question:
        return jsonify({"error": "file_path and question are required"}), 400

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    result = answer_question(file_path, question)
    return jsonify({
        "question": question,
        "answer": result["answers"]
    })


@app.route('/hackrx/run', methods=['POST'])
def run_query():
    data = request.get_json()
    doc_url = data.get("documents")
    questions = data.get("questions")

    # Download document
    file_name = "temp.pdf"
    response = requests.get(doc_url)
    with open(file_name, "wb") as f:
        f.write(response.content)

    all_answers = []
    for question in questions:
        result = answer_question(file_name, question)
        all_answers.extend(result["answers"])  # ✅ matches output format

    return jsonify({"answers": all_answers})

if __name__ == '__main__':
    app.run(debug=True)
