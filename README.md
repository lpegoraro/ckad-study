# CKAD Prep — Pegoraro's Agent for Study and Evaluate answers, test with local kubernetes (Docker Desktop)

This repository serves as both a session holder for me to return and summarize my mock exams for CKAD

Directory and how to store information.

```
 | ./sessions/ ## This will store the k8s resources YAMLs, CLI commands for imperative commands and the questions and answers in Markdown, to be the journal of my study
 |  |  ./agent-session1
 |  |  ./agent-session2
 |  |  ./ollama-session1
 |  |  ./warp-session1
```

After I some sessions, I will create some other with study guides, and helpers for summary and review topics.

## AI CKAD Instructor

This workspace contains an AI-focused study helper configured to act as a CKAD Instructor. Files to look at:

- `AGENT.md` — guidance for the local AI agent (prompts, rubric, and behavior rules).
- `.github/copilot-instructions.md` — concise instructions for Copilot-style agents working in this repo.
- `sessions/` — canonical source of exercises, manifests, and answers. Edit only after confirming with the agent.

Usage notes:

1. Install the recommended VS Code extensions (see `.vscode/extensions.json`).
2. Use the CKAD Instructor to generate mock tasks, evaluate your answers, or request progressive hints.
3. When the agent proposes YAML patches, it will supply a small diff you can apply under `sessions/`.

If you want the agent to work differently (different rubric, stricter constraints, or specific exam sources), update `AGENT.md` or ask the agent directly.

