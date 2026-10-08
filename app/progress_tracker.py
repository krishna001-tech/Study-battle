import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from app.models import Task


def load_tasks(path: str) -> List[Task]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Task(**task) for task in data["tasks"]]


def save_tasks(path: str, tasks: List[Task]) -> None:
    data = {"tasks": [task.__dict__ for task in tasks]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_progress_log(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_progress_log(path: str, entries: List[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def mark_task_complete(
    tasks_path: str,
    progress_log_path: str,
    subject: str,
    chapter: str,
    task_type: str,
    notes: str = "",
) -> Dict[str, Any]:
    tasks = load_tasks(tasks_path)
    for task in tasks:
        if (
            task.subject.lower() == subject.lower()
            and task.chapter.lower() == chapter.lower()
            and task.task_type.lower() == task_type.lower()
        ):
            task.status = "completed"
            entry = {
                "subject": task.subject,
                "chapter": task.chapter,
                "task_type": task.task_type,
                "completed_at": datetime.now().isoformat(timespec="minutes"),
                "notes": notes,
            }
            log = load_progress_log(progress_log_path)
            log.append(entry)
            save_tasks(tasks_path, tasks)
            save_progress_log(progress_log_path, log)
            return entry

    raise ValueError(f"Task not found: {subject} / {chapter} / {task_type}")


def get_completed_today(progress_log_path: str) -> List[Dict[str, Any]]:
    entries = load_progress_log(progress_log_path)
    today = datetime.now().date().isoformat()
    return [entry for entry in entries if entry["completed_at"].startswith(today)]


def build_progress_summary(tasks_path: str, progress_log_path: str) -> Dict[str, Any]:
    tasks = load_tasks(tasks_path)
    completed_count = sum(1 for task in tasks if task.status == "completed")
    pending_count = sum(1 for task in tasks if task.status != "completed")
    todays_complete = get_completed_today(progress_log_path)

    return {
        "completed_tasks": completed_count,
        "pending_tasks": pending_count,
        "completed_today": len(todays_complete),
        "latest_completed": todays_complete[-1] if todays_complete else None,
    }
