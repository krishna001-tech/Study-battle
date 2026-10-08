# JARVIS V1 MVP

A lightweight study assistant designed to decide the best next academic task based on urgency, priority, energy, and time available.

## Features

- Read user profile and subject status
- Read current task list
- Rank tasks by urgency and importance
- Adapt task difficulty to current energy level
- Return a single best next action
- Output a response in the JARVIS style

## Project structure

- app/models.py: data models
- app/decision_engine.py: ranking logic
- app/main.py: sample runner
- data/profile.json: profile data
- data/tasks.json: pending tasks

## Run

```bash
python -m venv .venv
source .venv/bin/activate
python app/main.py
```

## Example output

```text
Recommended next action:
- What to do: Work on Rotational Motion - advanced_problems.
- Duration: 45 minutes
- Why: This task is highest priority based on urgency, chapter weakness, and current schedule.
- After: Review mistakes and revise 2 weak formulas.
```
