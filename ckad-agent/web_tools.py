"""
Wrappers/examples for web-search and workspace search usage.

These functions are illustrative only: in VS Code Chat the agent uses built-in tools
(`web-search`, `semantic_search`, `read_file`, etc.). Keep these wrappers as
documentation and small helpers for local testing.
"""
from typing import List, Dict


def web_search_example(query: str, max_results: int = 5) -> List[Dict]:
    """Placeholder for web-search tool results."""
    # In the VS Code Chat environment, replace this with the 'web-search' tool call.
    return [{"title": "Kubernetes Docs - Deployments", "url": "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/", "snippet": "..."}]


def semantic_search_example(query: str, max_results: int = 5) -> List[Dict]:
    """Placeholder for workspace semantic search results."""
    return [{"file": "notes.md", "match": "example: use apps/v1 Deployment"}]
