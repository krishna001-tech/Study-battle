from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SubjectStatus:
    name: str
    current_chapter: str
    backlog: List[str] = field(default_factory=list)
    priority: int = 1


@dataclass
class Task:
    subject: str
    chapter: str
    task_type: str
    priority: int
    urgency: int
    estimated_minutes: int
    status: str = "not_started"
    deadline: Optional[str] = None
    notes: str = ""


@dataclass
class DailyContext:
    current_time: str
    available_minutes: int
    energy_level: str
    planned_tasks: List[str] = field(default_factory=list)
    completed_tasks: List[str] = field(default_factory=list)
    unfinished_tasks: List[str] = field(default_factory=list)


@dataclass
class UserProfile:
    name: str
    class_name: str
    exam: str
    goal: str
    subjects: List[SubjectStatus]
