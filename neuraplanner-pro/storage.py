"""
JSON-file persistence layer for NeuraPlanner Pro.

A single `data/tasks.json` file acts as the database. Each task record looks
like:

    {
        "id": 1,
        "title": "Write project README",
        "priority": "high",
        "completed": false,
        "created_at": "2025-01-15T09:24:11"
    }

The file is created automatically on first run.
"""
import json
import os
from datetime import datetime
from threading import Lock
from typing import Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "tasks.json")

# Guard file I/O so concurrent requests don't clobber each other.
_file_lock = Lock()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
def _ensure_storage() -> None:
    """Create the data directory and tasks.json on first run."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"tasks": [], "next_id": 1}, f, indent=2)


def _read() -> dict:
    _ensure_storage()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _write(data: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def get_tasks() -> list[dict]:
    """Return every task in insertion order."""
    with _file_lock:
        return _read()["tasks"]


def add_task(title: str, priority: str = "medium") -> dict:
    """Create a new task and return it."""
    with _file_lock:
        data = _read()
        task = {
            "id": data["next_id"],
            "title": title,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        data["tasks"].append(task)
        data["next_id"] += 1
        _write(data)
        return task


def mark_task_completed(task_id: int) -> Optional[dict]:
    """Flip the `completed` flag for the given task. Returns the task or None."""
    with _file_lock:
        data = _read()
        for task in data["tasks"]:
            if task["id"] == task_id:
                task["completed"] = True
                _write(data)
                return task
        return None
