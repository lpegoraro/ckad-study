"""
Simple CKAD study agent helpers — demonstration code.

This module contains example functions showing the intended calls the VS Code Chat agent
would orchestrate. In the VS Code Chat environment these calls are made via the built-in
tooling (web-search, semantic_search, read_file, apply_patch, run_in_terminal).

This file is a lightweight, runnable placeholder demonstrating the control flow.
"""
from typing import Dict, Any


def format_quiz_question(qid: int, prompt: str) -> Dict[str, Any]:
    return {"id": f"q{qid}", "prompt": prompt, "expected": None}


def study_question_flow(question: str) -> Dict[str, Any]:
    """Example flow (pseudocode for VS Code Chat agent integration).

    The real agent will call `web-search` and `semantic_search` via the VS Code agent tools.
    This function documents expected structure of returned data.
    """
    # Pseudocode placeholders showing what the agent will do
    web_results = "(web-search results placeholder)"
    local_notes = "(semantic_search results placeholder)"

    quick_answer = f"Short answer for: {question}"
    example_manifest = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: example
spec:
  replicas: 1
  selector:
    matchLabels:
      app: example
  template:
    metadata:
      labels:
        app: example
    spec:
      containers:
      - name: web
        image: nginx:stable
"""

    quiz = [format_quiz_question(1, "Create a Deployment with a single replica.")]

    return {
        "question": question,
        "quick_answer": quick_answer,
        "manifest": example_manifest,
        "web_results": web_results,
        "local_notes": local_notes,
        "quiz": quiz,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
    else:
        q = "How do I expose a Deployment with a LoadBalancer?"
    out = study_question_flow(q)
    print(out["quick_answer"]) 
# ckad-agent/main.py
import json
import os
from pathlib import Path

def handle_request(prompt: str):
    # 1. Web‑search
    results = web_search({"query": prompt, "max_results": 5})
    # 2. Semantic search in local notes
    local = semantic_search({"query": prompt, "max_results": 3})
    # 3. Return a combined answer
    return {
        "web": results,
        "local": local
    }