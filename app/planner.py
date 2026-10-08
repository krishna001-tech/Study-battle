import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from app.models import DailyContext, Task


def parse_clock(value: str) -> datetime:
    return datetime.strptime(value, "%H:%M")


def format_clock(value: datetime) -> str:
    return value.strftime("%H:%M")


def task_priority_score(task: Task) -> int:
    score = task.urgency * 10 + task.priority * 8

    heavy_tasks = {"advanced_problems", "test", "difficult_module"}
    if task.task_type in heavy_tasks:
        score += 5

    return score


def build_evening_plan(
    tasks: List[Task],
    available_minutes: int,
    energy_level: str = "medium",
    start_time: str = "18:00",
) -> List[Dict[str, Any]]:
    pending = [task for task in tasks if task.status != "completed"]
    if not pending:
        return []

    ranked = sorted(pending, key=task_priority_score, reverse=True)
    sessions: List[Dict[str, Any]] = []
    current_time = parse_clock(start_time)
    remaining = available_minutes

    for task in ranked:
        if remaining <= 0:
            break

        if energy_level == "low":
            session_minutes = min(task.estimated_minutes, 25)
        elif energy_level == "high":
            session_minutes = min(task.estimated_minutes, 60)
        else:
            session_minutes = min(task.estimated_minutes, 40)

        session_minutes = min(session_minutes, remaining)

        if session_minutes < 15:
            continue

        sessions.append(
            {
                "subject": task.subject,
                "chapter": task.chapter,
                "task_type": task.task_type,
                "start_time": format_clock(current_time),
                "duration_minutes": session_minutes,
                "reason": f"Priority {task.priority} / Urgency {task.urgency}",
            }
        )

        current_time += timedelta(minutes=session_minutes)
        remaining -= session_minutes

        if remaining >= 10 and task is not ranked[-1]:
            current_time += timedelta(minutes=5)
            remaining -= 5

    return sessions


def plan_evening(tasks: List[Task], daily_context: DailyContext) -> Dict[str, Any]:
    sessions = build_evening_plan(
        tasks,
        available_minutes=daily_context.available_minutes,
        energy_level=daily_context.energy_level,
        start_time="18:00",
    )

    if not sessions:
        return {
            "summary": "No realistic evening plan could be created.",
            "sessions": [],
            "total_minutes": 0,
        }

    total_minutes = sum(session["duration_minutes"] for session in sessions)
    return {
        "summary": f"Evening plan for {daily_context.available_minutes} minutes using {daily_context.energy_level} energy.",
        "sessions": sessions,
        "total_minutes": total_minutes,
    }
