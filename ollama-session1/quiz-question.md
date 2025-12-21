>>> I am preparing for CKAD exams, I am using a local k8s using Docker Desktop, and my study pattern is to deliver 
... YAMLs based on the --dry-run=client commands whenever available, and create a Namespace for each question, can 
... you quiz me?      
Thinking...
We need to quiz the user on CKAD. They want quiz. Provide YAML generation questions. Use local k8s, Docker 
Desktop, dry-run client, create Namespace per question. We can give multiple questions: create deployment, 
service, configmap, secret, pvc, etc. Provide scenario and ask to write YAML. They can test with dry-run. 
Should be interactive? Just provide questions.

We'll provide a list of questions, each requiring a YAML. Maybe 10 questions. Also include answer examples 
but maybe keep them separate? The user might want to test themselves. Provide scenario, ask for YAML. Provide 
the answer after they try? We can give answers at end. Or give in separate sections: questions first, answers 
after. We'll also explain how to apply dry-run.

Let's craft a set of questions covering various topics: deployments, statefulsets, jobs, services, ingress, 
configmaps, secrets, persistent volumes, liveness probes, environment variables, annotations, finalizers, 
resource limits, rolling update strategies, pod affinity, etc. They can use --dry-run=client -o yaml.

Let's provide each question, with a brief scenario, ask for YAML. Provide an answer with explanation. Let's 
format clearly.

We'll give 10-12 questions.

We can also include trick questions. Provide a namespace per question: namespace: question1, question2, etc. 
Use k8s version 1.28.

Ok, produce the quiz.
...done thinking.

Below is a “mini‑CKAD‑style” quiz that you can run locally in Docker‑Desktop.  
For every question create a **separate namespace** (e.g. `question-01`, `question-02`, …) so that the 
resources do not clash.  
Use the command template

```bash
kubectl apply -f - --dry-run=client -o yaml
```

to generate the manifest that would be applied.  
After you finish a question, scroll down to see the reference answer – copy it into your editor and run the 
dry‑run command to verify that it looks right.

> **Tip:** When you are ready to test the object, just remove the `--dry-run=client -o yaml` part and run  
> `kubectl apply -f <your‑file.yaml>`.

---

## 1️⃣  Simple Deployment (Read‑Only)

> **Scenario**  
> Create a Deployment called `hello-world` in namespace `question-01`.  
> It should run a single replica of the `nginx:1.25` image, expose port **80**, and mount a read‑only 
emptyDir volume called `cache` at `/usr/share/nginx/html`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world
  namespace: question-01
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
      - name: web
        image: nginx:1.25
        ports:
        - containerPort: 80
        volumeMounts:
        - name: cache
          mountPath: /usr/share/nginx/html
          readOnly: true
      volumes:
      - name: cache
        emptyDir: {}
```

---

## 2️⃣  ConfigMap Injection

> **Scenario**  
> In namespace `question-02` create a ConfigMap named `app-config` with two keys: `GREETING=Hello` and 
`TARGET=World`.  
> Then create a Deployment `greeted` that uses the config map as environment variables.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: question-02
data:
  GREETING: Hello
  TARGET: World
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: greeted
  namespace: question-02
spec:
  replicas: 1
  selector:
    matchLabels:
      app: greeted
  template:
    metadata:
      labels:
        app: greeted
    spec:
      containers:
      - name: app
        image: busybox
        command: ["sh", "-c", "echo ${GREETING}, ${TARGET}! && sleep 3600"]
        envFrom:
        - configMapRef:
            name: app-config
```

---

## 3️⃣  Secret (Opaque) and Environment Variable

> **Scenario**  
> Create an opaque Secret `db-secret` in `question-03` containing `username=admin` and `password=Pa$$w0rd`.  
> Deploy a pod `db-client` that reads those values into environment variables `DB_USER` and `DB_PASS`.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
  namespace: question-03
type: Opaque
data:
  username: YWRtaW4=            # base64(admin)
  password: QVBzZzB3PQ==        # base64(Pa$$w0rd)
---
apiVersion: v1
kind: Pod
metadata:
  name: db-client
  namespace: question-03
spec:
  containers:
  - name: client
    image: alpine
    command: ["sh", "-c", "echo ${DB_USER}:${DB_PASS} && sleep 3600"]
    env:
    - name: DB_USER
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: username
    - name: DB_PASS
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
```

---

## 4️⃣  Service with ClusterIP and NodePort

> **Scenario**  
> Create a Service named `api-service` in `question-04` that selects pods with label `app=api`.  
> It should expose port **8080** inside the cluster and map it to NodePort **32000**.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: question-04
spec:
  type: NodePort
  selector:
    app: api
  ports:
  - port: 8080
    targetPort: 8080
    nodePort: 32000
```

---

## 5️⃣  Ingress (TLS) with Path Routing

> **Scenario**  
> In `question-05`, create an Ingress that routes HTTP traffic to two services:  
> * `/blog` → `blog-service:80`  
> * `/api`  → `api-service:8080`  
> Assume TLS is already enabled on the cluster and use host `example.com`.  

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  namespace: question-05
spec:
  tls:
  - hosts:
    - example.com
  rules:
  - host: example.com
    http:
      paths:
      - path: /blog
        pathType: Prefix
        backend:
          service:
            name: blog-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
```

---

## 6️⃣  PersistentVolumeClaim & StatefulSet

> **Scenario**  
> In `question-06`, create a PVC named `data-pvc` requesting 1Gi of storage from a storage class `fast`.  
> Then create a StatefulSet `db` that uses this PVC as a mount at `/var/lib/db`.  
> The pod should run the `busybox` image and simply `sleep 3600`.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
  namespace: question-06
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: fast
  resources:
    requests:
      storage: 1Gi
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
  namespace: question-06
spec:
  serviceName: "db-headless"
  replicas: 1
  selector:
    matchLabels:
      app: db
  template:
    metadata:
      labels:
        app: db
    spec:
      containers:
      - name: db
        image: busybox
        command: ["sh", "-c", "sleep 3600"]
        volumeMounts:
        - name: data
          mountPath: /var/lib/db
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ReadWriteOnce]
      storageClassName: fast
      resources:
        requests:
          storage: 1Gi
```

---

## 7️⃣  Job with Backoff Limit

> **Scenario**  
> In `question-07`, create a Job named `once-job` that runs a single pod using the `alpine` image, executes 
`echo "Job succeeded!"`, and finishes.  
> Ensure that the job has a backoff limit of **0** (so it does not retry on failure).

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: once-job
  namespace: question-07
spec:
  backoffLimit: 0
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: job
        image: alpine
        command: ["sh", "-c", "echo 'Job succeeded!'"]
```

---

## 8️⃣  Liveness & Readiness Probes

> **Scenario**  
> Deploy a pod `web-app` in `question-08` that runs `nginx:1.25`.  
> Configure a liveness probe that checks `/healthz` on port 80 every 10s with a timeout of 3s.  
> Also configure a readiness probe that checks the same path every 5s with a timeout of 1s.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
  namespace: question-08
spec:
  containers:
  - name: nginx
    image: nginx:1.25
    ports:
    - containerPort: 80
    livenessProbe:
      httpGet:
        path: /healthz
        port: 80
      initialDelaySeconds: 15
      periodSeconds: 10
      timeoutSeconds: 3
    readinessProbe:
      httpGet:
        path: /healthz
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 5
      timeoutSeconds: 1
```

---

## 9️⃣  Pod Affinity (Same Node)

> **Scenario**  
> In `question-09`, create two deployments (`frontend` and `backend`) that should **run on the same node**.  
> Use pod affinity to achieve this. Each deployment runs a single replica of the `nginx:1.25` image on port 
80.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: question-09
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: question-09
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      affinity:
        podAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - frontend
            topologyKey: kubernetes.io/hostname
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
```

---

## 🔟  NetworkPolicy (Allow Only from a Specific Namespace)

> **Scenario**  
> In `question-10`, create a NetworkPolicy that **allows inbound traffic on port 80** only from pods in the 
namespace `trusted` that have the label `role:frontend`.  
> All other inbound traffic should be denied.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-trusted-frontend
  namespace: question-10
spec:
  podSelector: {}                      # Applies to all pods in question-10
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: trusted
      podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 80
```

> **Note:** If you want to deny all other traffic, make sure the default policy for the namespace is set to 
deny (e.g. via a `default-deny` policy).

---

### How to Verify

For each YAML file (e.g. `question-01.yaml`), run:

```bash
kubectl apply -f question-01.yaml --dry-run=client -o yaml
```

If the output matches the reference answer, you’re good to go.  
When you’re ready to actually create the resource, remove the `--dry-run=client -o yaml` flags and run:

```bash
kubectl apply -f question-01.yaml
```

---

Good luck on your CKAD prep! Feel free to tweak the scenarios (add resource limits, change image tags, etc.) 
to practice more edge‑cases. Happy quizzing!