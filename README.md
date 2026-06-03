# 🚀 DevOps 101 Task Manager

> **A complete, hands-on DevOps sandbox for freshers.**  
> Learn by doing — containerize, test, automate, and deploy a real-world web application.

![Task Manager Application](docs/assets/devops-101%20task%20manager.png)

---

## 📋 Table of Contents
1. [About the Project](#-about-the-project)
2. [Key Features](#-key-features)
3. [Prerequisites](#-prerequisites)
4. [Quick Start Installation](#-quick-start-installation)
5. [Usage](#-usage)
6. [Kubernetes & GitOps](#-kubernetes--gitops)
7. [Contributing](#-contributing)
8. [License](#-license)
9. [Contact & Support](#-contact--support)

---

## 🔍 About the Project

The **DevOps 101 Task Manager** is a simple, intuitive web application designed to help developers and system engineers learn the fundamentals of modern DevOps practices. 

The application is built using **Python and Flask**, providing a clean interface to create, track, and complete daily tasks. More importantly, the repository is pre-configured with a production-ready containerization structure, test suites, automated CI/CD pipelines, and monitoring tools to serve as an end-to-end learning sandbox.

---

## ✨ Key Features

* **Task Management:** Add, complete, and delete tasks dynamically.
* **Fully Containerized:** Built with a multi-stage Docker configuration for security and speed.
* **Automated Pipeline:** Linting, unit tests, and Docker Hub pushes configured with GitHub Actions.
* **Kubernetes Ready:** Manifests included for running and auto-scaling pods in local Kubernetes clusters.
* **Built-in Monitoring:** Ready-to-go dashboard setup with Prometheus and Grafana.

---

## 🛠️ Prerequisites

To run this project locally, you will need to have these tools installed:
* [Git](https://git-scm.com/) (Version Control)
* [Docker Desktop](https://www.docker.com/) (Container Engine)
* [Python 3.12+](https://www.python.org/) (To run without containers)

---

## ⚙️ Quick Start Installation

You can set up the application in two ways.

### Option 1: Run with Docker Compose (Recommended)
This method spins up the web application along with the monitoring tools automatically:

1. Open your terminal in the project directory.
2. Run the start command:
   ```bash
   docker compose up -d
   ```
3. Open your browser and visit:
   * **Task Manager App:** [http://localhost:5000](http://localhost:5000)
   * **Grafana Dashboard:** [http://localhost:3000](http://localhost:3000)
   * **Prometheus Dashboard:** [http://localhost:9090](http://localhost:9090)

To stop the application, run:
```bash
docker compose down
```

### Option 2: Run Locally (Without Docker)
1. Navigate to the app folder:
   ```bash
   cd app
   ```
2. Set up and activate a virtual environment:
   * **Windows:**
     ```powershell
     python -m venv .venv
     .venv\Scripts\activate
     ```
   * **macOS/Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. Install dependencies and run:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
4. Access the app at: [http://localhost:5000](http://localhost:5000)

> 💡 **For detailed step-by-step instructions, see the full [Installation Guide](docs/installation.md).**

---

## 💡 Usage

The Task Manager offers a web interface to interact with your tasks. It also features a REST API to query tasks programmatically.

### REST API Endpoints:
* `GET /api/tasks` — List all current tasks.
* `POST /api/tasks` — Create a new task (expects JSON: `{"title": "your task"}`).
* `PATCH /api/tasks/<id>` — Complete a task (expects JSON: `{"done": true}`).
* `DELETE /api/tasks/<id>` — Delete a task.

> 🧪 **To learn about running automated tests, coverage reports, and custom API requests, view the [Usage & API Guide](docs/usage.md).**

---

## ☸️ Kubernetes & GitOps

This repository is ready for Kubernetes deployments and GitOps workflows:
* The `k8s/` folder contains resource manifests for deployments, services, and horizontal pod auto-scalers.
* The pipeline is configured to automatically push changes and update Kubernetes configurations on GitHub.

> 📖 **Check out the [Kubernetes & GitOps Deployment Guide](docs/kubernetes.md) and the [Monitoring Guide](docs/monitoring.md) to set up Kubernetes, Argo CD, and dashboards.**

---

## 🤝 Contributing

We welcome contributions to improve this learning environment! Here is how you can help:

1. **Fork** the repository and clone it to your machine.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Add your changes and make sure tests pass: `pytest tests/ -v`.
4. Push your branch and open a **Pull Request**.

> 📜 **For our branching strategy, code styling requirements, and commit conventions, read the [Contributing Guidelines](docs/contributing.md).**

---

## 📄 License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute this software for educational and personal use.

---

## 📞 Contact & Support

If you have questions, feedback, or need help setting up:
* **GitHub Issues:** Open a ticket on our [GitHub Issues Page](https://github.com/Sanket006/devops-101-tasklab/issues) for bug reports and enhancements.
* **Maintainer:** Sanket ([GitHub/Sanket006](https://github.com/Sanket006))
* **Community:** Join discussions on GitHub for collaboration and Q&A.
