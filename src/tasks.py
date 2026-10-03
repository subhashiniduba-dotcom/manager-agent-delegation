"""
tasks.py - defines the ONE broad task given to the manager.

In CrewAI's hierarchical process we do NOT assign tasks to workers ourselves.
We give the manager one broad task, and the manager decides which worker
handles which part. That is what makes it real delegation.
"""
from crewai import Task


def create_main_task(goal: str) -> Task:
    description = f"""
The user's broad goal is:

"{goal}"

You are the manager. Do NOT write the specialist content yourself.
Break this goal into sub-tasks and DELEGATE each one to the correct coworker
using your delegation tool:

1. SQL Fundamentals Agent  -> the concept learning path (SELECT, WHERE, ORDER BY,
   GROUP BY, aggregates, filtering, joins), organised day by day.
2. SQL Practice Agent      -> practice exercises and mini challenges per week.
3. SQL Projects Agent      -> mini-project ideas, datasets and progression.
4. Learning Resources Agent-> resources, revision strategy, daily schedule,
   common mistakes.

(If the goal is not about SQL, adapt each worker's job to the new topic:
core concepts, practice, projects, resources.)

When every worker has answered, COMBINE their outputs into one final plan.
Do not just copy one worker's answer.
"""

    expected_output = """
A single Markdown document with exactly these sections:

# 2-Week Learning Plan
## Week 1  (Day 1 ... Day 7, each with topics and a practice item)
## Week 2  (Day 8 ... Day 14, each with topics and a practice item)
## Practice
## Projects
## Resources
## Final Advice

(Use a title and week count that match the user's actual goal.)
"""
    # No agent= here on purpose: the manager chooses who does what.
    return Task(description=description, expected_output=expected_output)
