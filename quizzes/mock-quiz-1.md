---
id: mock-quiz-1
topic: Services and Deployments
---

1. Create a Deployment named `web` with 2 replicas using the image `nginx:stable`.

Answer:
- manifest should use `apiVersion: apps/v1` and `kind: Deployment`.
- `spec.replicas` should equal `2` and selector/template labels must match.

2. Expose the `web` Deployment as a ClusterIP service on port 80.

Answer:
- Service `kind: Service`, `spec.type: ClusterIP`, `spec.ports` mapping `port: 80` to targetPort `80`.
