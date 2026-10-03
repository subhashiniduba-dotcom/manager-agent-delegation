"""
crew.py - assembles the Crew using the HIERARCHICAL process.

Key points:
  * manager_agent  -> our custom manager. It is NOT listed in agents=[...]
  * agents         -> only the workers
  * process        -> Process.hierarchical (manager delegates to workers)
"""
from crewai import Crew, Process

from src.agents import create_manager, create_workers
from src.tasks import create_main_task


def build_crew(goal: str, llm) -> Crew:
    manager = create_manager(llm)
    workers = create_workers(llm)
    main_task = create_main_task(goal)

    return Crew(
        agents=workers,
        tasks=[main_task],
        process=Process.hierarchical,
        manager_agent=manager,
        verbose=True,
    )
