"""
Smart planner and progress logic.

Kept deliberately simple for v1: the daily plan sorts pending tasks by
priority (high first) and assigns them to fixed focus blocks. A future
version could account for task duration, calendar conflicts, or energy
profiles - see the README for v2 ideas.
"""

# Lower number = higher priority when sorting.
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# Default focus blocks for a typical working day.
TIME_SLOTS = [
    "09:00 - 10:30",
    "10:45 - 12:00",
    "13:00 - 14:30",
    "14:45 - 16:00",
    "16:15 - 17:30",
]


def compute_progress(tasks: list[dict]) -> dict:
    """Return total / completed / remaining / percent for a task list."""
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    percent = round((completed / total) * 100) if total else 0
    return {
        "total": total,
        "completed": completed,
        "remaining": total - completed,
        "percent": percent,
    }


def build_daily_plan(tasks: list[dict]) -> list[dict]:
    """
    Pick the top pending tasks and lay them out across the day's focus blocks.

    Sort key: (priority rank, id) - so high-priority items come first, and
    among items of equal priority the oldest task wins.
    """
    pending = [t for t in tasks if not t["completed"]]
    pending.sort(key=lambda t: (PRIORITY_ORDER.get(t["priority"], 1), t["id"]))

    plan = []
    for slot, task in zip(TIME_SLOTS, pending[: len(TIME_SLOTS)]):
        plan.append(
            {
                "slot": slot,
                "task_id": task["id"],
                "title": task["title"],
                "priority": task["priority"],
            }
        )
    return plan
