# 🚀 DevOps 101 — End-to-End Beginner DevOps Project

> **A complete, hands-on DevOps sandbox for freshers.**
> Learn by doing — containerize, test, automate, and deploy a real application.

---

## 📦 What This Project Covers

| Concept | Tool Used | Version |
|---|---|---|
| 🐍 Application Development | Python + Flask | Flask 3.1.3 |
| 🐳 Containerization | Docker (multi-stage build) | Python 3.12-slim |
| 🔄 Local Orchestration | Docker Compose | v2+ (no version key) |
| ✅ Testing | pytest + pytest-cov | pytest 9.0.3 |
| ⚙️ CI/CD Pipeline | GitHub Actions | build-push-action v6 |
| ☸️ Container Orchestration | Kubernetes | autoscaling/v2 HPA |
| 📊 Monitoring | Prometheus + Grafana | Prom v3.11.3 / Grafana 13.0.1 |
| 💻 Version Control | Git + GitHub | — |

---

## 🗂️ Project Structure

```
devops-101-tasklab/
│
├── app/                          # 🐍 Application source code
│   ├── app.py                    # Flask application (API + UI)
│   ├── requirements.txt          # Runtime dependencies (Flask, gunicorn)
│   ├── requirements-dev.txt      # Dev/test dependencies (pytest, flake8)
│   ├── Dockerfile                # Multi-stage Docker build
│   └── .dockerignore             # Files to exclude from Docker
│
├── tests/                        # 🧪 Unit tests
│   └── test_app.py               # pytest test suite
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # ⚙️ GitHub Actions pipeline
│
├── k8s/                          # ☸️ Kubernetes manifests
│   ├── deployment.yaml           # Deployment, Service, ConfigMap, HPA
│   └── kind-config.yaml          # ☸️ Kind cluster port mapping configuration
│
├── docker-compose.yml            # 🔄 Full local stack
├── .gitignore                    # Git ignore rules
└── README.md                     # You are here!
```

---

## ⚡ Quick Start (5 Minutes)

### Prerequisites

Make sure you have installed:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
- [Git](https://git-scm.com/)
- Optional: [kubectl](https://kubernetes.io/docs/tasks/tools/) for Kubernetes

### 1. Clone the project

```bash
git clone https://github.com/YOUR_USERNAME/devops-101-tasklab.git
cd devops-101-tasklab
```

### 2. Run with Docker Compose (recommended for beginners)

```bash
docker compose up -d
```

That's it! Now open:

| Service | URL | Credentials |
|---|---|---|
| 🌐 Task Manager App | http://localhost:5000 | — |
| 📊 Grafana Dashboard | http://localhost:3000 | `admin` / `devops101` (default)* |
| 🔍 Prometheus | http://localhost:9090 | — |

*\* Note: You can customize the Grafana admin password by setting the `GRAFANA_ADMIN_PASSWORD` environment variable before running Docker Compose, e.g., `GRAFANA_ADMIN_PASSWORD=mysecurepassword docker compose up -d`.*

### 3. Stop the stack

```bash
docker compose down
```

---

## 🛠️ Running Locally (Without Docker)

```bash
# Navigate to app directory
cd app

# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit: http://localhost:5000

---

## 🧪 Running Tests

*Note: Make sure your virtual environment `.venv` is activated (see "Running Locally" step above) before installing dev dependencies.*

```bash
# Install dev dependencies (includes pytest, pytest-cov, flake8)
pip install -r app/requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=term-missing
```

Expected output:
```
PASSED tests/test_app.py::TestPageRoutes::test_index_returns_200
PASSED tests/test_app.py::TestPageRoutes::test_health_check
PASSED tests/test_app.py::TestPageRoutes::test_ready_check
PASSED tests/test_app.py::TestPageRoutes::test_metrics_endpoint
PASSED tests/test_app.py::TestTaskAPI::test_get_tasks
PASSED tests/test_app.py::TestTaskAPI::test_create_task
... 9 passed in 0.Xs
```

---

## 🐳 Docker Commands Cheatsheet

```bash
# Build the image manually
docker build -t devops101-app:v1 ./app

# Run the container
docker run -p 5000:5000 devops101-app:v1

# List running containers
docker ps

# View logs
docker logs <container_id>

# Stop the container
docker stop <container_id>

# Remove the container
docker rm <container_id>

# Remove the image
docker rmi devops101-app:v1
```

---

## ☸️ Kubernetes Deployment

### Prerequisites

- [minikube](https://minikube.sigs.k8s.io/docs/start/) or
- [kind](https://kind.sigs.k8s.io/) (Kubernetes in Docker)

### Start a local cluster

```bash
# Using minikube
minikube start

# OR using kind (with config for host port forwarding)
kind create cluster --config k8s/kind-config.yaml --name devops101
```

### Deploy the application

```bash
# 1. Edit k8s/deployment.yaml — replace YOUR_DOCKERHUB_USERNAME
#    with your actual DockerHub username

# 2. Apply the deployment manifest
kubectl apply -f k8s/deployment.yaml

# 3. Check everything is running
kubectl get all -n devops101

# 4. Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=devops101 -n devops101 --timeout=60s

# 5. Access the app (NodePort)
# If using minikube:
minikube service devops101-nodeport -n devops101
# If using kind: visit http://localhost:30080
```

### Useful kubectl commands

```bash
# Watch pod status in real-time
kubectl get pods -n devops101 -w

# View app logs
kubectl logs -l app=devops101 -n devops101 -f

# Describe a pod (for debugging)
kubectl describe pod -l app=devops101 -n devops101

# Scale the deployment manually
kubectl scale deployment devops101-app --replicas=3 -n devops101

# Delete everything
kubectl delete namespace devops101
```

### GitOps Deployment (Argo CD)

Instead of manually deploying manifests using `kubectl apply`, you can use GitOps to automatically synchronize changes from this repository using **Argo CD** deployed via Helm:

1. **Install Argo CD** via Helm:
   ```bash
   # Add the Helm repository
   helm repo add argo https://argoproj.github.io/argo-helm
   helm repo update

   # Install Argo CD
   helm install argocd argo/argo-cd --namespace argocd --create-namespace
   ```

2. **Configure your GitOps Application**:
   Apply the GitOps `Application` resource directly to the cluster to track your fork:
   ```bash
   kubectl apply -f - <<EOF
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: devops101-app
     namespace: argocd
   spec:
     project: default
     source:
       repoURL: 'https://github.com/Sanket006/devops-101-tasklab.git'
       targetRevision: main
       path: k8s
     destination:
       server: 'https://kubernetes.default.svc'
       namespace: devops101
     syncPolicy:
       automated:
         prune: true
         selfHeal: true
       syncOptions:
         - CreateNamespace=true
   EOF
   ```

3. **Access the Argo CD UI**:
   - Port-forward the API server to access the dashboard:
     ```bash
     kubectl port-forward svc/argocd-server -n argocd 8080:443
     ```
   - Open your browser to **[http://localhost:8080](http://localhost:8080)**.
   - Retrieve the `admin` password to log in:
     - **On Linux/Mac/Git Bash**:
       ```bash
       kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
       ```
     - **On Windows PowerShell**:
       ```powershell
       [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}")))
       ```

Argo CD will automatically create the `devops101` namespace and sync the application. Any subsequent commits pushed to Git (like tag updates by the CI/CD pipeline) will be automatically pulled and deployed to your cluster.

---

## ⚙️ CI/CD Pipeline (GitHub Actions)

The pipeline at `.github/workflows/ci-cd.yml` runs automatically on every `git push`.

### Pipeline Stages

```
git push
    │
    ▼
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌──────────┐
│  Lint   │ ──► │  Test   │ ──► │  Build  │ ──► │  Push   │ ──► │  Deploy  │
│ (flake8)│     │(pytest) │     │(Docker) │     │(DockerHub│     │(Update   │
│         │     │         │     │         │     │)        │     │ manifest)│
└─────────┘     └─────────┘     └─────────┘     └─────────┘     └──────────┘
```

> 📌 Push and Deploy stages only run on the `main` branch.

### Setting Up Secrets

Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**:

| Secret Name | Value |
|---|---|
| `DOCKERHUB_USERNAME` | Your DockerHub username |
| `DOCKERHUB_TOKEN` | Your DockerHub access token (NOT password!) |
| `REPO_TOKEN` | Your GitHub Personal Access Token (PAT) with repo scope (required to push manifest updates back to the repo) |

**Note:** Secret names in GitHub cannot start with `GITHUB_` (e.g., `GITHUB_PAT` is blocked), so this token is named `REPO_TOKEN`. We use a custom Personal Access Token (PAT) named `REPO_TOKEN` rather than the default, built-in `GITHUB_TOKEN` because commits pushed by `GITHUB_TOKEN` are blocked by GitHub from triggering downstream workflow runs. Using a PAT ensures that when the deploy stage updates the tag in `k8s/deployment.yaml`, the repository status successfully syncs with subsequent checks.

**How to get a DockerHub token:**
1. Login to hub.docker.com
2. Account Settings → Security → New Access Token
3. Copy the token and paste as the secret

---

## 📊 Monitoring (Kubernetes + Helm)

For Kubernetes environments, the monitoring stack is deployed via Helm using the standard `kube-prometheus-stack` chart, which installs Prometheus and Grafana.

### 1. Install Kube-Prometheus-Stack via Helm

```bash
# Add the Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install the stack with default settings
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

### 2. Verify Installation Status

Ensure that all monitoring pods are up and running:
```bash
kubectl get pods -n monitoring
```
*(Wait until all pods show `Running` or `Completed` status).*

### 3. Auto-Discovery (Scraping Metrics)

Prometheus automatically scrapes any pods carrying standard Prometheus annotations. Our Flask application pod in `k8s/deployment.yaml` is pre-configured with these annotations:
```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/path: "/metrics"
  prometheus.io/port: "5000"
```
Because of this, no additional Kubernetes custom resources (like `ServiceMonitor`) are needed.

### 4. Access Dashboards

- **Prometheus UI**:
  1. Port-forward the Prometheus service:
     ```bash
     kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090
     ```
  2. Open your browser to **[http://localhost:9090](http://localhost:9090)**.
  3. Try querying application metrics such as `tasks_total`, `tasks_done_total`, or `tasks_pending_total`.

- **Grafana UI**:
  1. Port-forward the Grafana service:
     ```bash
     kubectl port-forward svc/prometheus-grafana -n monitoring 3000:80
     ```
  2. Open your browser to **[http://localhost:3000](http://localhost:3000)**.
  3. Log in using the username `admin`.

### 5. Grafana Credentials

To retrieve the auto-generated `admin` password:

- **On Linux/Mac/Git Bash**:
  ```bash
  kubectl get secret --namespace monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
  ```
- **On Windows PowerShell**:
  ```powershell
  [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((kubectl get secret --namespace monitoring prometheus-grafana -o jsonpath="{.data.admin-password}")))
  ```

*(Alternatively, you can set a custom password during helm install/upgrade by adding `--set grafana.adminPassword="your-secure-password"`).*

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web UI |
| `GET` | `/health` | Liveness check (used by K8s) |
| `GET` | `/ready` | Readiness check (used by K8s) |
| `GET` | `/metrics` | Prometheus metrics |
| `GET` | `/api/tasks` | List all tasks |
| `POST` | `/api/tasks` | Create a task `{"title": "..."}` |
| `PATCH` | `/api/tasks/:id` | Update task `{"done": true}` |
| `DELETE` | `/api/tasks/:id` | Delete a task |

---

## 🎓 Learning Path

Follow this order to learn each concept step-by-step:

### Week 1 — App + Docker
- [ ] Run the app locally without Docker
- [ ] Read and understand `app/Dockerfile`
- [ ] Build the Docker image manually with `docker build`
- [ ] Run the container with `docker run`
- [ ] Read AND understand `docker-compose.yml`
- [ ] Start the full stack with `docker compose up`

### Week 2 — Testing + CI
- [ ] Run unit tests with `pytest`
- [ ] Read `tests/test_app.py` and understand each test
- [ ] Write 2 new tests yourself for the API
- [ ] Fork this repo to GitHub
- [ ] Add DockerHub secrets to your repo
- [ ] Push to `main` and watch the CI/CD pipeline run

### Week 3 — Kubernetes
- [ ] Install minikube / kind
- [ ] Read `k8s/deployment.yaml` top-to-bottom (all comments explained!)
- [ ] Deploy to local Kubernetes
- [ ] Scale the deployment manually
- [ ] Kill a pod and watch Kubernetes restart it
- [ ] Trigger a rolling update by changing the image tag

### Week 4 — Monitoring
- [ ] Query Prometheus for app metrics
- [ ] Create a Grafana dashboard
- [ ] Add an alert rule in Prometheus

---

## 📖 Glossary

| Term | Simple Explanation |
|---|---|
| **Container** | A lightweight, portable box that holds your app and everything it needs to run |
| **Docker** | The tool that creates and runs containers |
| **Image** | A blueprint/snapshot of a container |
| **Docker Compose** | A tool to run multiple containers together |
| **Kubernetes (K8s)** | A system that manages many containers across many machines |
| **Pod** | The smallest unit in Kubernetes — usually wraps one container |
| **Deployment** | A Kubernetes object that keeps a set of pods running |
| **Service** | A stable network endpoint that routes traffic to pods |
| **ConfigMap** | A way to store non-secret configuration in Kubernetes |
| **CI/CD** | Continuous Integration/Continuous Deployment — automating build, test, deploy |
| **GitHub Actions** | A CI/CD tool built into GitHub |
| **Prometheus** | A tool that collects and stores metrics from your app |
| **Grafana** | A tool that visualizes Prometheus metrics as dashboards |
| **Rolling Update** | Updating your app with zero downtime |
| **HPA** | Auto-scales pod count based on CPU/memory by load |
| **Liveness Probe** | K8s health check — restart pod if it fails |
| **Readiness Probe** | K8s health check — stop traffic to pod if it fails |

---

## 🙏 What You'll Learn

By completing this project, you will understand:

1. ✅ How to write a **real web API** with tests
2. ✅ How to **containerize** an app with a production-grade Dockerfile
3. ✅ How **CI/CD pipelines** work end-to-end
4. ✅ How **Kubernetes** manages containers: pods, services, scaling, probes
5. ✅ How **Prometheus + Grafana** monitor a live application
6. ✅ How **GitOps** works — a git push triggers the whole workflow

---

## 🤝 Contributing

We welcome contributions from the community to help improve this learning sandbox! To contribute:

1. **Fork** the repository to your own GitHub account.
2. **Clone** your fork locally and create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and ensure they adhere to the project's formatting standards.
4. **Run the test suite** locally to confirm everything passes:
   ```bash
   pytest tests/ -v
   ```
5. **Commit your changes** with a clear and concise commit message.
6. **Push** to your branch and submit a **Pull Request** to the `main` branch.

Please ensure your contributions focus on keeping the code simple, clear, and easy to understand for beginners.

---

## 📄 License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute this software for educational and personal use.

---

## 📞 Contact Information

If you have any questions, feedback, or need support while setting up the project:

- **GitHub Issues**: Open a ticket on our [Issues page](https://github.com/Sanket006/devops-101-tasklab/issues) for bug reports or feature suggestions.
- **Project Maintainer**: Sanket (Sanket006)
- **Community Forum**: Join our discussions on GitHub for Q&A and collaboration.

*Made with ❤️ for fresher DevOps engineers. Keep building, keep learning!*
