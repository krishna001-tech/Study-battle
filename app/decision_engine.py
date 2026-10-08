from typing import Any, Dict, List

from app.models import DailyContext, Task


def score_task(task: Task, daily_context: DailyContext) -> int:
    score = 0

    score += task.urgency * 25
    score += task.priority * 15

    if daily_context.energy_level == "low":
        if task.task_type in ["advanced_problems", "test", "difficult_module"]:
            score -= 20
        if task.task_type in ["concept_revision", "formula_revision", "basic_problems"]:
            score += 10

    if daily_context.energy_level == "high":
        if task.task_type in ["advanced_problems", "test"]:
            score += 10

    if task.estimated_minutes <= daily_context.available_minutes:
        score += 5
    else:
        score -= 10

    return score


def recommend_next_action(profile: Any, daily_context: DailyContext, tasks: List[Task]) -> Dict[str, Any]:
    pending = [task for task in tasks if task.status != "completed"]

    if not pending:
        return {
            "what_to_do": "Take a short break and review your backlog.",
            "duration_minutes": 10,
            "why": "There are no pending tasks right now.",
            "after": "Plan the next study block.",
            "report": "No tasks pending."
        }

    ranked = sorted(pending, key=lambda task: score_task(task, daily_context), reverse=True)
    best = ranked[0]

    if daily_context.energy_level == "low":
        if best.task_type in ["advanced_problems", "test"]:
            what_to_do = f"Do a short concept revision and 5 easy questions from {best.chapter}."
            duration = min(25, best.estimated_minutes)
            why = "Your energy is low, and the highest-value move is to keep momentum without exhausting yourself."
            after = "Then spend 10 minutes revising formulas or mistakes."
        else:
            what_to_do = f"Study {best.chapter} - {best.task_type}."
            duration = min(best.estimated_minutes, 30)
            why = "This is the best-ranked task and fits your current energy."
            after = "After this, do a quick recap of 2 formulas."
    else:
        what_to_do = f"Work on {best.chapter} - {best.task_type}."
        duration = min(best.estimated_minutes, 45)
        why = "This task is highest priority based on urgency, chapter weakness, and current schedule."
        after = "After completion, note mistakes and revise 2 weak formulas."

    return {
        "what_to_do": what_to_do,
        "duration_minutes": duration,
        "why": why,
        "after": after,
        "report": "When finished, report: what you solved, what was hard, and what to fix next."
    }
