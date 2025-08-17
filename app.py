from flask import Flask, request, jsonify
import os
from agents.task_executor import TaskExecutor

app = Flask(__name__)

# Initialize the AI agent
executor = TaskExecutor()

@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    task = data.get("task")

    if not task:
        return jsonify({"error": "Task not provided"}), 400

    try:
        result = executor.run(task)
        return jsonify({"task": task, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
