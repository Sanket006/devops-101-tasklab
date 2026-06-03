# Usage Guide & API Reference

This guide covers interacting with the Task Manager application, running the test suite, and basic development operations.

## 🌐 Web Interface

By default, when running the app locally or via Docker Compose, you can access the Task Manager UI by visiting:
**[http://localhost:5000](http://localhost:5000)**

From the UI, you can:
* Add new tasks with titles.
* Toggle tasks between "completed" and "pending".
* Delete tasks.

---

## 🔌 API Reference

The application exposes a RESTful API to manage tasks. All API payloads use the `application/json` format.

| Method | Endpoint | Description | Request Body Example | Response Code |
|---|---|---|---|---|
| **GET** | `/api/tasks` | Retrieves all tasks | None | `200 OK` |
| **POST** | `/api/tasks` | Creates a new task | `{"title": "Learn GitOps"}` | `201 Created` |
| **PATCH** | `/api/tasks/<id>` | Updates a task status | `{"done": true}` | `200 OK` |
| **DELETE** | `/api/tasks/<id>` | Deletes a specific task | None | `200 OK` |
| **GET** | `/health` | Liveness health check | None | `200 OK` |
| **GET** | `/ready` | Readiness check | None | `200 OK` |
| **GET** | `/metrics` | Prometheus metrics | None | `200 OK` |

### API Curl Examples

**Get All Tasks:**
```bash
curl -X GET http://localhost:5000/api/tasks
```

**Create a New Task:**
```bash
curl -X POST http://localhost:5000/api/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Configure Prometheus"}'
```

---

## 🧪 Testing & Linting

We use `pytest` for unit testing and `flake8` to enforce style guide consistency.

Before running tests, ensure your virtual environment is active and dev dependencies are installed:
```bash
pip install -r app/requirements-dev.txt
```

### 1. Run Unit Tests
To execute the tests with verbose output:
```bash
pytest tests/ -v
```

### 2. Run Test Coverage
To generate a terminal report showing code coverage details:
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

### 3. Run Linter
To verify code compliance with PEP 8 standards:
```bash
flake8 app/app.py --max-line-length=100 --ignore=E501,W503 --statistics
```

---

## 🐳 Docker CLI Cheatsheet

Here are common Docker commands useful during development:

```bash
# Build the image manually
docker build -t devops101-app:local ./app

# Run the container mapping host port 5000 to container port 5000
docker run -d -p 5000:5000 --name task-app devops101-app:local

# Inspect logs in real time
docker logs -f task-app

# Execute a bash session inside the running container
docker exec -it task-app bash

# Stop and remove the container
docker stop task-app
docker rm task-app
```
