Takeaways from first session yesterday

There's the need to review all kubectl commands and their organization
I need to be faster and also read some YAML configuration, and create a lot of example applications so I can be quick and save time in the exam.

Q1: 
Key Takeaways for CKAD:
•  Always include units for CPU (m for millicores) and memory (Mi, Gi, etc.)
•  Understand YAML hierarchy - restartPolicy is pod-level, not container-level
•  Valid restartPolicy values: Always (default), OnFailure, Never


Q2:
Key Takeaways for CKAD:
•  Use while loops with sleep for periodic tasks in containers - more reliable than watch
•  Multi-container pods share the same network namespace and can share volumes
•  Always specify -c <container-name> when getting logs from multi-container pods
•  The >> operator appends to files (vs > which overwrites)

Q3:
Key Takeaways for CKAD:
•  Never manually base64 encode with --from-literal - kubectl does it for you!
•  Use items: in ConfigMap volumes to mount specific keys only
•  Follow exact specifications (image tags, file contents) in exam questions
•  Your verification command technique is exam-gold - keep that approach!

Q4:
Key Takeaways for CKAD:
•  Always remove these fields from generated YAML before applying: generation, resourceVersion, uid, creationTimestamp, status
•  Labels must be consistent: Deployment metadata → selector → pod template
•  kubectl diff -f file.yaml compares file vs cluster (not file vs file)
•  --record flag stores command in annotations for rollout history (deprecated but still in exam)
•  Use k rollout history deployment/name to see revision history


Asked a Question to be faster
To generate a YAML faster, I can use the --dry-run=client and it will generate a YAML without the status and no runtime metadata (uid, resourceVersion, generation, creationTimestamp)
```sh
k get create deployment web-app --image=nginx:1.19 --replicas=3 \
    --dry-run=client -o yaml > web-app-deployment.yaml
```

export flag `--export` is deprecated in recent kubernetes versions.

There is also a neat plugin, that is definetly to enhance my day to day but not for CKAD

Q5: 
Key Takeaways for CKAD:
•  Always verify your work with functional tests (curl, wget, etc.)
•  Services use selectors to find pods - labels must match!
•  ClusterIP = internal only, NodePort = external access
•  --dry-run=client creates clean YAML every time
•  Remove status: fields from YAML before applying
•  Test pod-to-service connectivity with kubectl exec ... -- curl

Notes: I had some issues on connecting, cause I misslabeled the services and once it was fixed, I didn't understand how to access via NodePort. Mostly cause Docker Desktop K8s auto published the IP from `k get nodes -o wide` and this is not documented, so I had just to curl -v localhost:<node-port> and it worked.

Why This Happens:

| Cluster Type | NodePort Access Method |
|--------------|------------------------|
| Docker Desktop | localhost:30080 |
| Minikube | minikube ip:30080 or minikube service |
| Kind | Need port mapping or localhost:30080 |
| Cloud (GKE/EKS/AKS) | <node-external-ip>:30080 |
| Real cluster | Any node IP:30080 |

For CKAD Exam:
The exam environment typically uses standard clusters where you can access NodePort via the node's IP. But knowing these variations is helpful for practice!

