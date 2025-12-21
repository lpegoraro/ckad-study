#!/usr/bin/env python3
"""Simple CLI wrapper to grade a quiz using `grader.py`."""
import json
import sys
from pathlib import Path
from grader import grade_quiz, pretty_feedback


def main():
    if len(sys.argv) < 3:
        print("Usage: grade_cli.py <quiz.md> <answers.json>")
        sys.exit(2)
    quiz = sys.argv[1]
    answers_file = sys.argv[2]
    p = Path(answers_file)
    if not p.exists():
        print(f"Answers file not found: {answers_file}")
        sys.exit(2)
    answers = json.loads(p.read_text())
    results = grade_quiz(quiz, answers)
    print(pretty_feedback(results))


if __name__ == "__main__":
    main()
