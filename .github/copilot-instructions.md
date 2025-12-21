<!-- Copilot / AI agent guidance for this repo -->
# Repo-specific instructions for AI coding agents

This repository contains a small CKAD study agent and example quizzes. The goal
is to help AI coding agents be immediately productive by documenting the
project structure, conventions, workflows, and concrete examples.

Key components
- `ckad-agent/`: agent helper code and small runnable examples (`main.py`,
  `web_tools.py`, `grader.py`, `grade_cli.py`). The agent flow is demonstrated
  in `ckad-agent/main.py`.
- `quizzes/`: markdown quizzes used by the grader. Example: `mock-quiz-1.md` and
  `sample_answers.json`.

Big-picture architecture and data flow
- User prompt -> agent uses VS Code Chat tools: `web-search`, `semantic_search`,
  `read_file` to gather context (see `ckad-agent/main.py` for the illustrative
  control flow).
- Agent produces short answers and example manifests (YAML strings) and may
  generate quizzes. For grading, the flow is: quiz markdown -> `grader.parse_quiz_markdown()`
  -> expected bullets -> `grade_expected_bullets()` compares user answers.

Project conventions and patterns (explicit and discoverable)
- Quiz markdown format: numbered questions (`1. Question text`), followed by an
  `Answer:` header and `-` bullet lines for expected key points. See
  `quizzes/mock-quiz-1.md` and `ckad-agent/grader.py::parse_quiz_markdown()`.
- Grading logic: keyword-based matching. `grader.py` normalizes text,
  strips punctuation, removes STOPWORDS, and checks whether at least one
  significant keyword from each expected bullet appears in the user's answer.
  Avoid relying on exact phrasing.
- Local helpers in `ckad-agent/web_tools.py` are illustrative only — in the
  VS Code Chat runtime you must use the provided tools (`web-search`,
  `semantic_search`, `read_file`, `apply_patch`, `run_in_terminal`).

Developer workflows (concrete commands)
- Run the demo agent locally (placeholder behavior):

```bash
python ckad-agent/main.py "How do I create a Deployment with a PVC?"
```

- Grade a quiz locally using the CLI wrapper:

```bash
python ckad-agent/grade_cli.py quizzes/mock-quiz-1.md quizzes/sample_answers.json
```

Integration points and external dependencies
- No external packages are required; the code uses Python stdlib only.
- The intended integration runtime is VS Code Chat (agent tools listed above).
- Agent definitions (for loading into VS Code Chat) are expected under
  `.github/agents/` (the README references `.github/agents/ckad-exam-prep.agent.md`).

Guidance for making code edits and patches
- Keep patches small and focused (the repo examples and the grader expect
  stable file paths and quiz formats).
- When altering quiz parsing or grading behavior, add/update `quizzes/*.md`
  examples and include a `sample_answers.json` demonstrating the expected
  answer keys (IDs like `q1`, `q2`).
- When the agent requests `apply_patch`, prefer edits that preserve public
  functions in `ckad-agent/` (e.g., `grade_quiz`, `parse_quiz_markdown`) to
  avoid breaking local testing.

Concrete examples for the agent to reference
- To extract quiz questions: use `ckad-agent/grader.py::parse_quiz_markdown()`.
- To grade answers programmatically: call `ckad-agent/grader.py::grade_quiz(quiz_path, answers_dict)`
  and format with `pretty_feedback()` for human-readable output.

If anything here is unclear or you'd like more detail about a specific
component (e.g., intended VS Code Chat agent configuration under
`.github/agents/`), tell me which area and I will update this file.
