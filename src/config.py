"""
config.py - loads settings from the .env file and builds the LLM.

WHY: Secrets (API key) must never be written in source code.
We read them from environment variables instead.
"""
import os
import sys

from dotenv import load_dotenv
from crewai import LLM

# Reads the .env file in the project folder and puts its values into os.environ
load_dotenv()

DEFAULT_GOAL = "Create a 2-week study plan for learning SQL from beginner to intermediate level."


def get_llm() -> LLM:
    """Create the Gemini LLM that ALL agents (manager + workers) will use."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()

    if not api_key or api_key == "your_api_key_here":
        print("\n[ERROR] GEMINI_API_KEY is missing.")
        print("Fix: create a file named .env in the project folder and add:")
        print("     GEMINI_API_KEY=your_real_key")
        print("Get a free key at https://aistudio.google.com/apikey")
        sys.exit(1)

    # The "gemini/" prefix tells CrewAI which provider to use.
    return LLM(
        model=f"gemini/{model}",
        api_key=api_key,
        temperature=0.4,
    )
