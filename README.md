import json
from pathlib import Path

from app.decision_engine import recommend_next_action
from app.models import DailyContext, SubjectStatus, Task, UserProfile
from app.planner import plan_evening


def load_profile(path: str) -> UserProfile:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    subjects = [SubjectStatus(**subject) for subject in data["subjects"]]
    return UserProfile(
        name=data["name"],
        class_name=data["class_name"],
        exam=data["exam"],
        goal=data["goal"],
        subjects=subjects,
    )


def load_tasks(path: str) -> list[Task]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [Task(**task) for task in data["tasks"]]


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    profile = load_profile(str(base_dir / "data" / "profile.json"))
    tasks = load_tasks(str(base_dir / "data" / "tasks.json"))

    daily_context = DailyContext(
        current_time="19:30",
        available_minutes=120,
        energy_level="medium",
        planned_tasks=["Physics chapter revision", "Chemistry MCQs"],
        completed_tasks=["Maths homework"],
        unfinished_tasks=["Physics chapter test prep"],
    )

    action = recommend_next_action(profile, daily_context, tasks)
    plan = plan_evening(tasks, daily_context)

    print("Recommended next action:")
    print(f"- What to do: {action['what_to_do']}")
    print(f"- Duration: {action['duration_minutes']} minutes")
    print(f"- Why: {action['why']}")
    print(f"- After: {action['after']}")
    print()

    print("Evening plan:")
    print(f"- Summary: {plan['summary']}")
    for session in plan["sessions"]:
        print(
            f"  * {session['start_time']} - {session['subject']} / {session['chapter']} / {session['task_type']} "
            f"({session['duration_minutes']} min)"
        )


if __name__ == "__main__":
    main()
