# NeuraPlanner Pro

> A focused productivity planner that turns your task list into a structured day.
> Built with Flask, vanilla JavaScript, and a single JSON file for storage — no database, no build step, no framework lock-in.

![Stack: Flask + Vanilla JS](https://img.shields.io/badge/stack-Flask%20%2B%20Vanilla%20JS-c5f02b)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Overview

**NeuraPlanner Pro** is a small but production-style web app designed as a portfolio project. It demonstrates:

- A thin, well-separated Flask REST API
- A vanilla-JS single-page UI (no framework, no bundler)
- File-based JSON persistence with a thread-safe write layer
- A simple "smart planner" that schedules pending tasks into focus blocks by priority

The codebase is intentionally beginner-readable but organized like a real project: business logic lives in dedicated modules (`storage.py`, `planner.py`), the Flask file (`app.py`) stays thin, and the frontend is split across HTML, CSS, and JS files.

---

## Features

### Task management
- Add tasks via the UI with a priority of `low`, `medium`, or `high`
- View every task in a clean, sortable list
- Mark tasks as completed with one click

### Smart daily planner
- Automatically generates a day plan from your pending tasks
- Sorts by priority (high first), then by age
- Lays tasks out across five fixed focus blocks (09:00 → 17:30)
- Regenerate at any time with the **Regenerate** button

### Progress tracker
- Live progress bar
- Percent complete + count of remaining tasks
- Updates instantly when a task is checked off

---

## Project structure

```
neuraplanner-pro/
├── app.py                  # Flask app + route definitions
├── storage.py              # JSON persistence (thread-safe)
├── planner.py              # Daily plan + progress logic
├── data/
│   └── tasks.json          # Auto-created on first run
├── static/
│   ├── style.css           # Editorial dark theme
│   └── app.js              # Frontend logic (fetch + DOM)
├── templates/
│   └── index.html          # Single-page UI
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How to run locally

### 1. Clone and enter the project

```bash
git clone https://github.com/<your-username>/neuraplanner-pro.git
cd neuraplanner-pro
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the server

```bash
python app.py
```

### 5. Open the app

Visit **http://127.0.0.1:5000** in your browser.

The first time you add a task, `data/tasks.json` is created automatically.

---

## API endpoints

The backend exposes a small REST API. All endpoints return JSON.

| Method | Endpoint         | Description                                              |
| ------ | ---------------- | -------------------------------------------------------- |
| GET    | `/get_tasks`     | Returns every task in insertion order.                   |
| POST   | `/add_task`      | Creates a new task. Body: `{ "title": str, "priority": "low\|medium\|high" }` |
| POST   | `/complete_task` | Marks a task completed. Body: `{ "id": int }`            |
| GET    | `/get_progress`  | Returns `{ total, completed, remaining, percent }`.      |
| GET    | `/get_plan`      | Returns the generated daily plan.                        |

### Examples

**Add a task**

```bash
curl -X POST http://127.0.0.1:5000/add_task \
  -H "Content-Type: application/json" \
  -d '{"title": "Write project README", "priority": "high"}'
```

Response:

```json
{
  "task": {
    "id": 1,
    "title": "Write project README",
    "priority": "high",
    "completed": false,
    "created_at": "2025-01-15T09:24:11"
  }
}
```

**Mark a task as completed**

```bash
curl -X POST http://127.0.0.1:5000/complete_task \
  -H "Content-Type: application/json" \
  -d '{"id": 1}'
```

**Fetch progress**

```bash
curl http://127.0.0.1:5000/get_progress
```

```json
{ "total": 5, "completed": 2, "remaining": 3, "percent": 40 }
```

---

## Design notes

- **Storage**: A single `tasks.json` file under `/data` acts as the database. Reads and writes are guarded by a `threading.Lock` so concurrent requests in the dev server don't corrupt the file. For anything beyond a single-user dev setup, swap this layer for SQLite or Postgres — `storage.py` is the only file you'd need to touch.
- **Planner**: The "smart" planner is intentionally simple. It sorts pending tasks by priority and slots them into fixed time blocks. The interface (`build_daily_plan`) is the seam where an AI-powered scheduler could plug in.
- **Frontend**: No framework. The whole UI is one HTML file, one CSS file, and one JS file. Every action triggers a full `refresh()` that pulls tasks, progress, and plan in parallel — simple to reason about and fast enough for a single user.

---

## Roadmap — ideas for v2

If you want to extend this project, here are natural next steps in roughly increasing order of effort:

### 🔐 Authentication
- Add per-user accounts so multiple people can use one deployment.
- Use Flask-Login for session management and Flask-WTF for CSRF protection.
- Hash passwords with `bcrypt` or use OAuth (Google, GitHub) via `Authlib`.

### 🗄️ Real database
- Replace the JSON layer with SQLite via SQLAlchemy — same interface, transactional safety, indexes, migrations.
- For production, swap the SQLAlchemy URL to Postgres and add Alembic for migrations.

### 🧠 AI integration
- Use the Anthropic API in `planner.py` to generate smarter daily plans — for example, accepting natural-language goals ("focus day, ship the API") and ordering tasks accordingly.
- Add a "summarize my day" endpoint that uses an LLM to produce an end-of-day recap.
- Auto-tag and prioritize incoming tasks from a one-line description.

### 📅 Calendar & duration
- Add `estimated_minutes` to each task and pack the daily plan against a real time budget.
- Sync with Google Calendar via the Calendar API to avoid scheduling over meetings.

### 🔔 Notifications & recurrence
- Recurring tasks ("every weekday", "every Monday").
- Browser notifications when a focus block starts.

### 📈 Analytics
- Weekly completion trends, average tasks completed per day, productivity by hour.
- Export to CSV.

### 🧪 Testing & CI
- Add `pytest` with tests for `storage.py` and `planner.py` (pure functions — easy to test).
- GitHub Actions workflow that runs lint + tests on every push.

### 🚀 Deployment
- Containerize with Docker (one `Dockerfile`, multistage build).
- Deploy to Fly.io, Render, or Railway with a single command.

---

## License

MIT — do whatever you want, attribution appreciated.
