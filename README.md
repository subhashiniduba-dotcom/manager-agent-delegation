# Manager Agent with Delegation

## Overview
A multi-agent system built with **Python + CrewAI**. A **Manager Agent** receives ONE broad goal
(default: *"Create a 2-week study plan for learning SQL from beginner to intermediate level."*),
splits it into sub-tasks, **delegates** them to specialist **Worker Agents**, collects their outputs
and merges everything into one final plan saved in `output/final_plan.md`.

## Architecture
```
USER
 |
 v
MANAGER AGENT  (CrewAI hierarchical process)
 |-----> SQL FUNDAMENTALS AGENT
 |-----> SQL PRACTICE AGENT
 |-----> SQL PROJECTS AGENT
 |-----> LEARNING RESOURCES AGENT
 v
MANAGER COLLECTS RESULTS
 v
FINAL COMBINED STUDY PLAN  ->  output/final_plan.md
```

## Features
- 1 manager + 4 workers
- Real delegation via `Process.hierarchical` (workers are not called manually)
- Interactive goal input (works for other goals too, e.g. "Plan a 3-day trip to Goa")
- API key kept in `.env` (never committed)
- Friendly error hints

## Technology Stack
Python 3.10-3.13, CrewAI 1.x, Google Gemini (free tier via Google AI Studio), python-dotenv.

## Project Structure
```
manager-agent-delegation/
├── main.py            # entry point
├── requirements.txt
├── .env.example       # template (real key goes in .env)
├── .gitignore
├── src/
│   ├── config.py      # loads .env, builds the Gemini LLM
│   ├── agents.py      # manager + worker agents
│   ├── tasks.py       # the one broad task
│   └── crew.py        # Crew with hierarchical process
├── output/final_plan.md
└── docs/GUIDE.md      # setup, recording script, viva, troubleshooting
```

## How It Works
1. `main.py` asks for a goal.
2. `crew.py` builds a Crew with `process=Process.hierarchical` and `manager_agent=manager`.
3. The manager reads the single task and uses CrewAI's built-in **"Delegate work to coworker"** tool to send sub-tasks to workers.
4. Each worker answers independently and returns text to the manager.
5. The manager merges the answers into the final Markdown plan.

## Manager Agent
Role: *Multi-Agent Study Plan Manager*. It has `allow_delegation=True` and is passed as `manager_agent`
(it is NOT in the `agents` list).

## Worker Agents
### SQL Fundamentals Agent
Day-by-day concepts: SELECT, WHERE, ORDER BY, GROUP BY, aggregates, filtering, joins.
### SQL Practice Agent
Exercises, query-writing drills, mini challenges.
### SQL Projects Agent
Mini-project ideas, datasets, progression, portfolio focus.
(Plus a 4th worker: **Learning Resources Agent** – resources, revision, common mistakes.)

## Installation
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Environment Variables
```bat
copy .env.example .env
```
Edit `.env`:
```
GEMINI_API_KEY=your_real_key
GEMINI_MODEL=gemini-2.5-flash
```
Free key: https://aistudio.google.com/apikey

## Running the Project
```bat
python main.py
```

## Example Input
`Create a 2-week study plan for learning SQL from beginner to intermediate level.`

## Example Output
See `output/final_plan.md` after a run (sections: Week 1, Week 2, Practice, Projects, Resources, Final Advice).

## Delegation Flow
Look in the terminal for CrewAI logs showing the manager agent starting, then
`Delegate work to coworker` tool calls naming each worker, each worker's own run,
and finally the manager's final answer.

## Screenshots
Add screenshots of the terminal logs and `final_plan.md` here (e.g. `docs/screenshot1.png`).

## Future Improvements
- Add web-search tools for workers
- Run workers in parallel
- Add a simple web UI
- Per-agent models

## License
MIT
