# Installation and Setup Guide

This guide will walk you through setting up your environment and running the DevOps 101 Task Manager application.

## Prerequisites

Before starting, ensure you have the following tools installed on your system:

| Tool | Purpose | Recommended Version | Install Link |
|---|---|---|---|
| **Git** | Version control & repository management | Latest | [git-scm.com](https://git-scm.com/) |
| **Python** | Running the Flask application locally | `3.12+` | [python.org](https://www.python.org/) |
| **Docker Desktop** | Building, running containerized app & Compose | Latest | [docker.com](https://www.docker.com/products/docker-desktop/) |
| **Kubectl** | Interacting with Kubernetes clusters | Latest | [kubernetes.io](https://kubernetes.io/docs/tasks/tools/) |
| **Helm** | Deploying monitoring and GitOps tools in K8s | `v3+` | [helm.sh](https://helm.sh/) |

---

## 1. Clone the Repository

Begin by cloning your fork of the project repository to your local machine:

```bash
git clone https://github.com/Sanket006/devops-101-tasklab.git
cd devops-101-tasklab
```

---

## 2. Option A: Local Run (No Docker)

For rapid development, you can run the Flask application directly on your host machine.

### Windows (PowerShell)
1. **Navigate to the app directory:**
   ```powershell
   cd app
   ```
2. **Create a Python Virtual Environment:**
   ```powershell
   python -m venv .venv
   ```
3. **Activate the Virtual Environment:**
   ```powershell
   .venv\Scripts\activate
   ```
4. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
5. **Run the App:**
   ```powershell
   python app.py
   ```

### macOS / Linux (Bash/Zsh)
1. **Navigate to the app directory:**
   ```bash
   cd app
   ```
2. **Create a Python Virtual Environment:**
   ```bash
   python3 -m venv .venv
   ```
3. **Activate the Virtual Environment:**
   ```bash
   source .venv/bin/activate
   ```
4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the App:**
   ```bash
   python app.py
   ```

Once started, the application will be accessible at: **[http://localhost:5000](http://localhost:5000)**

---

## 3. Option B: Local Container Run (Docker Compose)

Running the application using Docker Compose is the recommended way to stand up the entire stack, including monitoring components.

1. **Verify Docker is running:**
   Make sure Docker Desktop is started and running.

2. **Start the stack:**
   Run the following command in the root of the project:
   ```bash
   docker compose up -d
   ```

3. **Verify the services:**
   Ensure the containers are active:
   ```bash
   docker compose ps
   ```

This will spin up:
- The Task Manager web app at `http://localhost:5000`
- Prometheus server at `http://localhost:9090`
- Grafana dashboard at `http://localhost:3000`

To tear down the containers and cleanup network resources:
```bash
docker compose down
```
