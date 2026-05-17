"""
NeuraPlanner Pro - Flask application entry point.

Exposes a small REST API for managing tasks and serves the single-page UI.
Keep this file thin: business logic lives in `storage.py` and `planner.py`.
"""
from flask import Flask, jsonify, render_template, request

from planner import build_daily_plan, compute_progress
from storage import add_task, get_tasks, mark_task_completed

app = Flask(__name__)


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Render the single-page UI."""
    return render_template("index.html")


# ---------------------------------------------------------------------------
# Task API
# ---------------------------------------------------------------------------
@app.route("/get_tasks", methods=["GET"])
def api_get_tasks():
    """Return every task in insertion order."""
    return jsonify({"tasks": get_tasks()})


@app.route("/add_task", methods=["POST"])
def api_add_task():
    """
    Create a new task.

    Expected JSON body:
        { "title": "Write README", "priority": "low|medium|high" }
    """
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    priority = (data.get("priority") or "medium").lower()

    if not title:
        return jsonify({"error": "Task title is required"}), 400
    if priority not in {"low", "medium", "high"}:
        priority = "medium"

    task = add_task(title=title, priority=priority)
    return jsonify({"task": task}), 201


@app.route("/complete_task", methods=["POST"])
def api_complete_task():
    """
    Mark a task as completed.

    Expected JSON body:
        { "id": 1 }
    """
    data = request.get_json(silent=True) or {}
    task_id = data.get("id")

    if task_id is None:
        return jsonify({"error": "Task id is required"}), 400

    task = mark_task_completed(int(task_id))
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"task": task})


# ---------------------------------------------------------------------------
# Planner / progress
# ---------------------------------------------------------------------------
@app.route("/get_progress", methods=["GET"])
def api_get_progress():
    """Return completion statistics."""
    return jsonify(compute_progress(get_tasks()))


@app.route("/get_plan", methods=["GET"])
def api_get_plan():
    """Return a generated daily plan based on the current task list."""
    return jsonify({"plan": build_daily_plan(get_tasks())})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
