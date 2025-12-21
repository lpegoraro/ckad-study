---
name: ckad-study-agent
display_name: CKAD Study Agent (workspace)
description: |
  Lightweight agent to help study CKAD topics. Uses the local `mcp.json`
  tool definitions (web-search, semantic_search, read_file, apply_patch,
  run_in_terminal) and provides `study` and `mock_quiz` commands.
mcp: ../mcp.json
---

# Importing this agent into VS Code Chat

Save this file and then in VS Code:

- Open the **VS Code Chat** pane (View → Chat or the Chat icon).
- Click the Agents menu (three-dots or the agent picker) → **Import agent from workspace**.
- Select this file: `.github/agents/ckad-exam-prep.agent.md`.
- After import you should see an agent named **CKAD Study Agent (workspace)**
  available in the agent selector.

# Quick usage examples

- Ask a study question (use the `study` command):

```text
study question:"How do I create a Deployment with a PVC?"
```

- Generate a small mock quiz:

```text
mock_quiz topic:"persistent volumes" count:5
```

# Troubleshooting

- If the agent doesn't appear after import: reload the window (`Developer: Reload Window`).
- Ensure the workspace root contains `mcp.json` (this repo has `/mcp.json`).
- If import fails, open the file and ensure it is saved under `.github/agents/`.

# Notes for agent authors

- This agent relies on the `mcp.json` at the repo root. The `ckad-agent/`
  folder contains runnable examples and local graders (`grader.py`, `grade_cli.py`).
- Keep the `mcp.json` in sync with any changes to available commands or tools.
