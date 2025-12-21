# CKAD Agent helper

This folder contains example code and instructions to integrate a CKAD study agent with VS Code Chat.

Overview
- `main.py` — small runnable placeholder that demonstrates the study question flow.
- `web_tools.py` — illustrative wrappers showing the shape of `web-search` and `semantic_search` results.

Usage
1. Open VS Code Chat and import the agent defined under `.github/agents/ckad-exam-prep.agent.md`.
2. Use the `study` or `mock_quiz` commands (configured by `mcp.json`) from inside VS Code Chat.

Local testing
Run the example flow locally (this doesn't perform network searches — it's a placeholder):

```bash
python ckad-agent/main.py "How do I create a Deployment with a PVC?"
```

Integrations
- The VS Code Chat runtime will provide `web-search`, `semantic_search`, `read_file`, `apply_patch`, and `run_in_terminal`.
- When requesting patches or terminal runs, always review the suggested changes and outputs before applying.
