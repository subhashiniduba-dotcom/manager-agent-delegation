"""
main.py - entry point. Run with:  python main.py
"""
import os
import sys
import traceback

from src.config import DEFAULT_GOAL, get_llm
from src.crew import build_crew

LINE = "=" * 60


def explain_error(err: Exception) -> None:
    """Print a beginner-friendly hint for common errors."""
    text = str(err).lower()
    print(f"\n[ERROR] {type(err).__name__}: {err}\n")
    if "api key" in text or "api_key" in text or "401" in text or "403" in text or "permission" in text:
        print("Hint: Your API key looks invalid. Create a new one at https://aistudio.google.com/apikey and update .env")
    elif "429" in text or "rate" in text or "quota" in text or "resource_exhausted" in text:
        print("Hint: Rate limit / quota reached on the free tier. Wait 1-2 minutes and run again.")
    elif "404" in text or "not found" in text or "model" in text:
        print("Hint: Model name problem. In .env set GEMINI_MODEL=gemini-2.5-flash (or another available model).")
    elif "connection" in text or "timeout" in text or "network" in text or "getaddrinfo" in text:
        print("Hint: Network problem. Check your internet connection and try again.")
    else:
        print("Hint: See docs/GUIDE.md -> Troubleshooting. Full details below:")
        traceback.print_exc()


def main() -> None:
    print(LINE)
    print("MANAGER AGENT WITH DELEGATION")
    print(LINE)

    goal = input("\nEnter your goal (press Enter for default):\n> ").strip() or DEFAULT_GOAL
    print(f"\nBroad Goal:\n{goal}\n")

    llm = get_llm()  # exits with a clear message if the API key is missing

    print("[Our message] Manager: delegating tasks...")
    print("[Our message] CrewAI will now print its own logs (Agent Started / Tool Usage / Task Completed).")
    print("[Our message] Look for 'Delegate work to coworker' lines - that is the real delegation.\n")

    try:
        crew = build_crew(goal, llm)
        result = crew.kickoff()
    except Exception as err:
        explain_error(err)
        sys.exit(1)

    final_text = str(result)

    print("\n" + LINE)
    print("FINAL COMBINED PLAN")
    print(LINE)
    print(final_text)

    os.makedirs("output", exist_ok=True)
    with open(os.path.join("output", "final_plan.md"), "w", encoding="utf-8") as f:
        f.write(final_text)
    print(f"\n[Our message] Saved to output{os.sep}final_plan.md")


if __name__ == "__main__":
    main()
