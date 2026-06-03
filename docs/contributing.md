# Contributing Guidelines

Thank you for contributing to the DevOps 101 Task Manager project! This guide explains how to get started, our development workflow, and the coding standards we enforce.

## 🌿 Branching Model

We follow a simple Git branching model to manage changes:

* **`main`**: Represents the stable, production-ready release state. All automated deployments (Docker Hub push, manifest updates) trigger here.
* **`develop`**: The integration branch for new features. All pull requests are merged here first before moving to `main`.
* **`feature/*`**: Short-lived branches created for specific features, bug fixes, or documentation tasks (e.g., `feature/add-metrics-endpoint`).

---

## 🚀 Step-by-Step Contribution Flow

### 1. Fork and Clone
1. Fork the repository to your own GitHub account by clicking the **Fork** button.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/simple-devops-project.git
   cd simple-devops-project
   ```

### 2. Create a Feature Branch
Create a branch starting from `develop` for your changes:
```bash
git checkout develop
git checkout -b feature/your-feature-name
```

### 3. Make Changes and Test Locally
1. Make your changes in the codebase.
2. Activate your virtual environment and install the development dependencies:
   ```bash
   pip install -r app/requirements-dev.txt
   ```
3. Run the linter to verify formatting:
   ```bash
   flake8 app/app.py --max-line-length=100 --ignore=E501,W503 --statistics
   ```
4. Run the test suite:
   ```bash
   pytest tests/ -v
   ```

### 4. Commit and Push
1. Stage your changes:
   ```bash
   git add .
   ```
2. Commit with a clear, concise message describing what was done:
   ```bash
   git commit -m "feat: add task due date parameter to task schema"
   ```
3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

### 5. Create a Pull Request
1. Navigate to the original repository on GitHub.
2. Click **New Pull Request**.
3. Select `develop` as the base branch and `feature/your-feature-name` from your fork as the compare branch.
4. Fill out the PR description template details and submit.

---

## 📝 Commit Message Guidelines

We use semantic commit messages to make the git history readable and easy to scan:

* **`feat:`** A new feature or capability (e.g., `feat: add prometheus metric for tasks`).
* **`fix:`** A bug fix (e.g., `fix: resolve db session leaks`).
* **`docs:`** Documentation-only changes (e.g., `docs: create contributing guide`).
* **`refactor:`** A code change that neither fixes a bug nor adds a feature (e.g., `refactor: clean up git deployment step`).
* **`test:`** Adding missing tests or correcting existing tests (e.g., `test: add unit test for health endpoint`).

---

## 🎨 Coding Standards

To ensure the repository remains simple, educational, and maintainable for beginners, please follow these principles:
* Keep functions small and focused on a single responsibility.
* Write docstrings for all key functions, routes, and tests.
* Avoid complex third-party library dependencies unless strictly necessary.
* Ensure all code modifications include corresponding unit tests in the `tests/` directory.
