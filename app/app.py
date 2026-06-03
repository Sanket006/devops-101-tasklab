"""
DevOps 101 - Simple Task Manager App
A beginner-friendly Flask web application to demonstrate the full DevOps lifecycle.
"""

import os
import logging
from flask import Flask, request, jsonify, render_template_string, abort
from datetime import datetime, timezone

# --- App Configuration ---
app = Flask(__name__)
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
app.config['VERSION'] = os.environ.get('APP_VERSION', '1.0.0')
app.config['ENV_NAME'] = os.environ.get('ENV_NAME', 'development')

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# --- In-memory task store (no DB needed for this demo) ---
tasks = [
    {"id": 1, "title": "Learn Docker", "done": True, "created_at": "2024-01-01"},
    {"id": 2, "title": "Write a Dockerfile", "done": True, "created_at": "2024-01-02"},
    {"id": 3, "title": "Set up GitHub Actions CI", "done": False, "created_at": "2024-01-03"},
    {"id": 4, "title": "Deploy to Kubernetes", "done": False, "created_at": "2024-01-04"},
    {"id": 5, "title": "Add Prometheus monitoring", "done": False, "created_at": "2024-01-05"},
]
next_id = 6

# ─────────────────────────────────────────────────────────────────────────────
#  HTML Template (Single Page App embedded in Python for simplicity)
# ─────────────────────────────────────────────────────────────────────────────
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>DevOps 101 | Task Manager</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0d1117; --surface: #161b22; --border: #30363d;
      --accent: #58a6ff; --accent2: #3fb950; --danger: #f85149;
      --text: #e6edf3; --muted: #8b949e;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }
    .header { background: var(--surface); border-bottom: 1px solid var(--border);
              padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; }
    .header h1 { font-size: 1.4rem; font-weight: 700; }
    .header h1 span { color: var(--accent); }
    .badge { background: #21262d; border: 1px solid var(--border); border-radius: 20px;
             padding: 0.2rem 0.8rem; font-size: 0.75rem; color: var(--muted); }
    .container { max-width: 800px; margin: 2rem auto; padding: 0 1rem; }
    .info-bar { display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }
    .info-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
                 padding: 1rem 1.5rem; flex: 1; min-width: 140px; }
    .info-card .label { font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
    .info-card .value { font-size: 1.5rem; font-weight: 700; margin-top: 0.3rem; }
    .add-form { display: flex; gap: 0.8rem; margin-bottom: 2rem; }
    .add-form input { flex: 1; background: var(--surface); border: 1px solid var(--border);
                      border-radius: 8px; padding: 0.8rem 1rem; color: var(--text);
                      font-family: inherit; font-size: 1rem; outline: none; transition: border-color 0.2s; }
    .add-form input:focus { border-color: var(--accent); }
    .add-form button { background: var(--accent); color: #0d1117; border: none; border-radius: 8px;
                       padding: 0.8rem 1.5rem; font-weight: 600; cursor: pointer;
                       font-family: inherit; font-size: 1rem; transition: opacity 0.2s; }
    .add-form button:hover { opacity: 0.85; }
    .task-list { display: flex; flex-direction: column; gap: 0.6rem; }
    .task { background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
            padding: 1rem 1.2rem; display: flex; align-items: center; gap: 1rem;
            transition: border-color 0.2s, transform 0.1s; }
    .task:hover { border-color: var(--accent); transform: translateX(3px); }
    .task.done { opacity: 0.55; }
    .task.done .task-title { text-decoration: line-through; }
    .task-check { width: 20px; height: 20px; cursor: pointer; accent-color: var(--accent2); }
    .task-title { flex: 1; font-size: 1rem; }
    .task-date { font-size: 0.75rem; color: var(--muted); }
    .task-del { background: none; border: none; color: var(--danger); cursor: pointer;
                font-size: 1.1rem; padding: 0.2rem 0.4rem; border-radius: 4px;
                transition: background 0.2s; }
    .task-del:hover { background: rgba(248,81,73,0.15); }
    .footer { text-align: center; color: var(--muted); font-size: 0.8rem; margin-top: 3rem; padding: 2rem; }
    .env-pip { display: inline-block; background: #21262d; border: 1px solid var(--border);
               border-radius: 4px; padding: 0.15rem 0.5rem; font-family: monospace; font-size: 0.8rem; }
  </style>
</head>
<body>
  <div class="header">
    <h1>⚙️ DevOps <span>101</span> Task Manager</h1>
    <div class="badge">v{{ version }} · {{ env_name }}</div>
  </div>
  <div class="container">
    <div class="info-bar">
      <div class="info-card">
        <div class="label">Total Tasks</div>
        <div class="value" id="total">-</div>
      </div>
      <div class="info-card">
        <div class="label">Completed</div>
        <div class="value" style="color:var(--accent2)" id="done">-</div>
      </div>
      <div class="info-card">
        <div class="label">Pending</div>
        <div class="value" style="color:var(--accent)" id="pending">-</div>
      </div>
    </div>
    <div class="add-form">
      <input id="newTask" type="text" placeholder="Add a new DevOps task…" />
      <button onclick="addTask()">Add Task</button>
    </div>
    <div class="task-list" id="taskList"></div>
    <div class="footer">
      Running on env: <span class="env-pip">{{ env_name }}</span> &nbsp;|&nbsp;
      💡 Learn DevOps by doing — containerize, automate, deploy!
    </div>
  </div>
  <script>
    async function loadTasks() {
      const res = await fetch('/api/tasks');
      const tasks = await res.json();
      const list = document.getElementById('taskList');
      list.innerHTML = '';
      let done = 0;
      tasks.forEach(t => {
        if (t.done) done++;
        const el = document.createElement('div');
        el.className = 'task' + (t.done ? ' done' : '');
        el.innerHTML = `
          <input class="task-check" type="checkbox" ${t.done ? 'checked' : ''}
                 onchange="toggleTask(${t.id}, this.checked)" />
          <span class="task-title"></span>
          <span class="task-date"></span>
          <button class="task-del" onclick="deleteTask(${t.id})">✕</button>`;
        el.querySelector('.task-title').textContent = t.title;
        el.querySelector('.task-date').textContent = t.created_at;
        list.appendChild(el);
      });
      document.getElementById('total').textContent = tasks.length;
      document.getElementById('done').textContent = done;
      document.getElementById('pending').textContent = tasks.length - done;
    }
    async function addTask() {
      const inp = document.getElementById('newTask');
      const title = inp.value.trim();
      if (!title) return;
      await fetch('/api/tasks', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({title})
      });
      inp.value = '';
      loadTasks();
    }
    async function toggleTask(id, done) {
      await fetch(`/api/tasks/${id}`, {
        method: 'PATCH', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({done})
      });
      loadTasks();
    }
    async function deleteTask(id) {
      await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
      loadTasks();
    }
    document.getElementById('newTask').addEventListener('keydown', e => {
      if (e.key === 'Enter') addTask();
    });
    loadTasks();
  </script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────────────────────────────────────────


@app.route('/')
def index():
    logger.info("Serving index page")
    return render_template_string(HTML_TEMPLATE,
                                  version=app.config['VERSION'],
                                  env_name=app.config['ENV_NAME'])


@app.route('/health')
def health():
    """Health check endpoint — used by Kubernetes liveness probe."""
    return jsonify({"status": "healthy", "version": app.config['VERSION'], "time": str(datetime.now(timezone.utc))}), 200


@app.route('/ready')
def ready():
    """Readiness check endpoint — used by Kubernetes readiness probe."""
    return jsonify({"status": "ready"}), 200


@app.route('/metrics')
def metrics():
    """Basic Prometheus-compatible text-format metrics."""
    total = len(tasks)
    done = sum(1 for t in tasks if t['done'])
    metrics_text = f"""# HELP tasks_total Total number of tasks
# TYPE tasks_total gauge
tasks_total {total}
# HELP tasks_done_total Completed tasks
# TYPE tasks_done_total gauge
tasks_done_total {done}
# HELP tasks_pending_total Pending tasks
# TYPE tasks_pending_total gauge
tasks_pending_total {total - done}
"""
    return metrics_text, 200, {'Content-Type': 'text/plain; charset=utf-8'}


# ─── Task CRUD API ────────────────────────────────────────────────────────────

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


@app.route('/api/tasks', methods=['POST'])
def create_task():
    global next_id
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, description="Invalid request payload. Must be a JSON object.")
    title = data.get('title')
    if not isinstance(title, str) or not title.strip():
        abort(400, description="Task title is required and must be a string")
    task = {
        "id": next_id,
        "title": title.strip(),
        "done": False,
        "created_at": datetime.now(timezone.utc).strftime('%Y-%m-%d')
    }
    tasks.append(task)
    next_id += 1
    logger.info(f"Created task: {task['title']}")
    return jsonify(task), 201


@app.route('/api/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        abort(404, description=f"Task {task_id} not found")
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, description="Invalid request payload. Must be a JSON object.")
    if 'done' in data:
        task['done'] = bool(data['done'])
    if 'title' in data:
        title = data['title']
        if not isinstance(title, str) or not title.strip():
            abort(400, description="Task title must be a non-empty string")
        task['title'] = title.strip()
    logger.info(f"Updated task {task_id}")
    return jsonify(task)


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    original_len = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]
    if len(tasks) == original_len:
        abort(404, description=f"Task {task_id} not found")
    logger.info(f"Deleted task {task_id}")
    return jsonify({"deleted": task_id}), 200


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting DevOps 101 app on port {port}")
    app.run(host='0.0.0.0', port=port)
