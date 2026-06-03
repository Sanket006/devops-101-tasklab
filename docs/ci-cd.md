# CI/CD Pipeline Guide (GitHub Actions)

This guide documents the automated Continuous Integration and Continuous Deployment (CI/CD) pipeline built with GitHub Actions in [.github/workflows/ci-cd.yml](file:///c:/Users/Lenovo/Sanket%20Personal/simple-devops-project/.github/workflows/ci-cd.yml).

## 🔄 Workflow Pipeline Overview

The pipeline automatically triggers on:
* **Pushes** to `main` and `develop` branches.
* **Pull requests** targeting the `main` branch.

```
                  git push / PR
                       │
                       ▼
┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐      ┌──────────┐
│  Lint   │ ───> │  Test   │ ───> │  Build  │ ───> │  Push   │ ───> │  Deploy  │
│ (flake8)│      │(pytest) │      │(Docker) │      │(Docker  │      │(Update   │
│         │      │         │      │         │      │ Hub)    │      │ manifest)│
└─────────┘      └─────────┘      └─────────┘      └─────────┘      └──────────┘
                                                        ▲                ▲
                                                        │                │
                                                   (Only main)      (Only main)
```

---

## 🛠️ Pipeline Jobs & Stages

### 1. Lint (`lint`)
* **Runs on:** `ubuntu-latest`
* **Checks:** Performs code syntax and style analysis using `flake8` against python files.
* **Goal:** Ensures clean code formatting before running tests.

### 2. Test (`test`)
* **Runs on:** `ubuntu-latest` (depends on `lint`)
* **Checks:** Runs the python test suite using `pytest`.
* **Output:** Generates a coverage report uploaded as an artifact (`coverage-report`).

### 3. Build (`build`)
* **Runs on:** `ubuntu-latest` (depends on `test`)
* **Action:** Compiles the Docker image, tags it using Git meta tags, and caches layers using GitHub Actions cache (`type=gha`).
* **Output:** Outputs the built tags and Git SHA. Provenance is disabled (`provenance: false`) to avoid compatibility issues with Docker registries.

### 4. Push (`push`)
* **Runs on:** `ubuntu-latest` (depends on `build`)
* **Action:** Logs into Docker Hub using secrets, compiles the final multi-tag image, and pushes it to Docker Hub.
* **Execution:** Only executes on pushes to the `main` branch.

### 5. Deploy (`deploy`)
* **Runs on:** `ubuntu-latest` (depends on `push`)
* **Action:** GitOps-style deployment. 
  1. Checks out the code using a custom Personal Access Token (`REPO_TOKEN`).
  2. Replaces the Docker image tag inside `k8s/deployment.yaml` with the newly pushed tag using `sed`.
  3. Git-attributes the commit dynamically using your GitHub credentials (`github.actor`).
  4. Commits and pushes the updated file back to the remote `main` branch.
* **Execution:** Only executes on pushes to the `main` branch.

---

## 🔑 GitHub Repository Secrets Configuration

For the pipeline to run successfully, you must configure the following Secrets in your GitHub repository (**Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**):

| Secret Name | Purpose | Example / Details |
|---|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub Account username | e.g. `sanket006` |
| `DOCKERHUB_TOKEN` | A personal access token generated on Docker Hub | Generate from Account Settings -> Security -> New Access Token |
| `REPO_TOKEN` | A GitHub Personal Access Token (PAT) with `repo` scope | Required because the default `GITHUB_TOKEN` is blocked from triggering downstream workflows when committing back. |

---

## 🚀 The GitOps Loop & Local Syncing

Because the `deploy` job commits the updated `k8s/deployment.yaml` file back to the remote repository, **your local repository will become one commit behind the remote main branch** every time a pipeline run finishes.

### Syncing your local repo:
Before you make new local changes or push again, always pull and rebase to merge the manifest updates:
```bash
git pull --rebase
```
This keeps your local workspace in sync with the automated commits made by the pipeline.
