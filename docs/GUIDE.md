# Windows Guide

## 1. Check environment
```bat
python --version
pip --version
git --version
cd
```
Python must be 3.10-3.13. If a command is "not recognized": install Python from python.org (tick **Add Python to PATH**) or Git from git-scm.com, then reopen the terminal.

## 2. Setup
```bat
cd manager-agent-delegation
python -m venv .venv
.venv\Scripts\activate          (CMD)
.venv\Scripts\Activate.ps1      (PowerShell; if blocked run: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned)
```
Active venv shows `(.venv)` at the start of the prompt.
```bat
pip install -r requirements.txt
pip show crewai
```
## 3. API key
1. Open https://aistudio.google.com/apikey, sign in, click **Create API key**.
2. `copy .env.example .env` then paste the key into `.env`.
3. Verify: `python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(bool(os.getenv('GEMINI_API_KEY')))"` -> `True`

## 4. Run and test
```bat
python main.py
```
Press Enter for the default SQL goal. Success = CrewAI logs, a final plan printed, and `output\final_plan.md` created.

**Proof of delegation (point at these in the logs):**
- Manager agent box: "Multi-Agent Study Plan Manager" starting the task
- Tool usage: **Delegate work to coworker** (appears per worker, with the coworker name)
- Agent boxes for SQL Fundamentals / Practice / Projects / Resources agents each doing their own work
- Manager's final answer combining everything
Note: lines starting with `[Our message]` are ours; all boxes/tool logs are CrewAI's.

## 5. Git / GitHub
Create an empty repo on github.com (no README), copy its URL.
```bat
git init
git status
```
Confirm `.env` is NOT listed, then:
```bat
git add .
git commit -m "Build manager agent with worker delegation"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```
Check key not committed: `git ls-files | findstr .env` should show only `.env.example`.
If a key was ever committed: delete that key in AI Studio and create a new one.

## 6. Recording script (3-5 min)
| Time | Show | Say |
|---|---|---|
| 0:00-0:20 | GitHub repo + README title | "This is a manager-worker multi-agent system using CrewAI." |
| 0:20-0:50 | Folder structure | "main.py runs it; src has agents, tasks, crew, config." |
| 0:50-1:20 | agents.py | "One manager with allow_delegation=True and four workers with different roles." |
| 1:20-1:50 | crew.py | "Process.hierarchical plus manager_agent means the manager delegates; I don't call workers manually." |
| 1:50-2:00 | .env exists (don't open it) | "The API key is in .env, ignored by Git." |
| 2:00-3:30 | `python main.py`, press Enter | Point at manager start, Delegate work to coworker lines, worker outputs |
| 3:30-4:00 | Final plan in terminal | "The manager merged all worker outputs." |
| 4:00-4:20 | output/final_plan.md | "Saved result." |
| 4:20-5:00 | GitHub again | "Code is pushed; .env is not in the repo." |

## 7. Troubleshooting
| Error | Cause | Fix / verify |
|---|---|---|
| `ModuleNotFoundError` | venv not active or packages missing | `.venv\Scripts\activate` then `pip install -r requirements.txt`; verify `python -c "import crewai"` |
| `ImportError` | wrong/old CrewAI version | `pip install -U "crewai[google-genai]"`; verify `pip show crewai` |
| `'python' is not recognized` | Python not on PATH | Reinstall with Add to PATH; try `py --version` |
| API key not found | `.env` missing/misnamed | Must be named exactly `.env` in project root with `GEMINI_API_KEY=...` |
| `AuthenticationError` / 401 / 403 | invalid key | Create new key, update `.env` |
| `RateLimitError` / 429 | free-tier limit | Wait 1-2 min, rerun; free tier has per-minute/day caps |
| Model not found / 404 | bad model name | Set `GEMINI_MODEL=gemini-2.5-flash` in `.env` |
| Connection error | no internet/proxy | Check network, retry |
| CrewAI process error | manager included in `agents` or missing `manager_agent` | Keep manager only in `manager_agent=` |
| `AttributeError` | old tutorial code/version mismatch | Use this repo's code; `pip install -U crewai` |
| `ValidationError` | wrong field in Agent/Task/Crew | Check field names against the files here |
| PowerShell script blocked | execution policy | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |

## 8. Viva Q&A
1. **Multi-agent system?** Several AI agents working together on one goal.
2. **AI agent?** An LLM with a role, goal and ability to act/decide.
3. **Manager agent?** The agent that splits the goal, delegates and combines results.
4. **Worker agent?** A specialist that completes one assigned sub-task.
5. **Why multiple agents?** Specialisation gives better, more organised results.
6. **Delegation?** The manager assigning a sub-task to another agent.
7. **Hierarchical process?** Manager-led workflow; manager assigns and reviews tasks.
8. **Why CrewAI?** Simple Python framework with built-in roles, tasks and manager delegation.
9. **CrewAI Agent?** Object with role, goal, backstory, LLM.
10. **CrewAI Task?** A unit of work with description and expected output.
11. **CrewAI Crew?** The team: agents + tasks + process.
12. **How does the manager talk to workers?** Through CrewAI's "Delegate work to coworker" and "Ask question to coworker" tools.
13. **How does it choose a worker?** The LLM matches the sub-task to each worker's role/goal/backstory.
14. **After workers finish?** Their text returns to the manager.
15. **How are outputs combined?** The manager LLM merges them into the format in `expected_output`.
16. **Why not one agent?** One agent mixes everything and gives shallower results; splitting improves focus.
17. **If a worker fails?** The error appears in the logs; the manager can retry or the run stops; we print a hint and exit.
18. **Which LLM?** Google Gemini (gemini-2.5-flash) via the free AI Studio API.
19. **Where is the API key?** In `.env`, loaded by python-dotenv, ignored by Git.
20. **Future improvements?** Search tools, parallel workers, web UI, memory, per-agent models.
21. **Why is the manager not in `agents`?** It is supplied separately as `manager_agent`.
22. **Why `allow_delegation=False` on workers?** So only the manager delegates and workers do the work.

## 9. Final checklist
[ ] Python installed  [ ] venv created and active  [ ] CrewAI installed  [ ] `.env` configured
[ ] `.gitignore` ok  [ ] Agents + tasks created  [ ] Hierarchical process  [ ] Delegation tested
[ ] final_plan.md generated  [ ] README done  [ ] Key NOT committed  [ ] GitHub pushed  [ ] Recording done
