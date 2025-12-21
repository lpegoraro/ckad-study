# Grader usage

This file documents how to run the grader locally.

1. Edit or create an answers JSON file mapping question ids to your answers. Example `quizzes/sample_answers.json`:

```json
{
  "q1": "A Deployment named web using apiVersion apps/v1 and kind Deployment with spec.replicas set to 2 and matching labels.",
  "q2": "Create a Service of kind Service with spec.type ClusterIP and port 80 mapping to targetPort 80."
}
```

2. Run the grader CLI:

```bash
python3 ckad-agent/grade_cli.py quizzes/mock-quiz-1.md quizzes/sample_answers.json
```

3. The grader will print per-question feedback and an overall percentage score.

Notes and limitations
- The grader performs keyword-based checks against expected bullets in the quiz markdown. It is intended to give quick, actionable feedback, not a perfect semantic grading.
- To improve accuracy, enhance the `expected` bullets in your quiz files with concise, unambiguous key points.
