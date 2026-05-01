"""
Unit tests for the DevOps 101 Task Manager App.
Run with: pytest tests/ -v
"""

import pytest
import json
import sys
import os

# Add the app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.app import app as flask_app, tasks


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


# ─── Page Routes ─────────────────────────────────────────────────────────────

class TestPageRoutes:

    def test_index_returns_200(self, client):
        """Home page should load successfully."""
        res = client.get('/')
        assert res.status_code == 200
        assert b'DevOps' in res.data

    def test_health_check(self, client):
        """Health endpoint must return 200 with healthy status."""
        res = client.get('/health')
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data['status'] == 'healthy'

    def test_ready_check(self, client):
        """Readiness endpoint must return 200."""
        res = client.get('/ready')
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data['status'] == 'ready'

    def test_metrics_endpoint(self, client):
        """Metrics endpoint should return Prometheus text format."""
        res = client.get('/metrics')
        assert res.status_code == 200
        assert b'tasks_total' in res.data


# ─── Task API ─────────────────────────────────────────────────────────────────

class TestTaskAPI:

    def test_get_tasks(self, client):
        """GET /api/tasks should return a list."""
        res = client.get('/api/tasks')
        assert res.status_code == 200
        data = json.loads(res.data)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_create_task(self, client):
        """POST /api/tasks should create a new task."""
        payload = {"title": "Test task via pytest"}
        res = client.post('/api/tasks',
                          data=json.dumps(payload),
                          content_type='application/json')
        assert res.status_code == 201
        data = json.loads(res.data)
        assert data['title'] == "Test task via pytest"
        assert data['done'] is False
        assert 'id' in data

    def test_create_task_missing_title(self, client):
        """POST /api/tasks without title should return 400."""
        res = client.post('/api/tasks',
                          data=json.dumps({}),
                          content_type='application/json')
        assert res.status_code == 400

    def test_create_task_empty_title(self, client):
        """POST /api/tasks with empty title should return 400."""
        res = client.post('/api/tasks',
                          data=json.dumps({"title": "   "}),
                          content_type='application/json')
        assert res.status_code == 400

    def test_update_task_status(self, client):
        """PATCH /api/tasks/:id should mark task as done."""
        # Use the first existing task (id=1)
        res = client.patch('/api/tasks/1',
                           data=json.dumps({"done": True}),
                           content_type='application/json')
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data['done'] is True

    def test_update_nonexistent_task(self, client):
        """PATCH on nonexistent task should return 404."""
        res = client.patch('/api/tasks/99999',
                           data=json.dumps({"done": True}),
                           content_type='application/json')
        assert res.status_code == 404

    def test_delete_task(self, client):
        """DELETE /api/tasks/:id should remove the task."""
        # First create a task to delete
        payload = {"title": "Task to delete"}
        create_res = client.post('/api/tasks',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        task_id = json.loads(create_res.data)['id']
        # Now delete it
        del_res = client.delete(f'/api/tasks/{task_id}')
        assert del_res.status_code == 200

    def test_delete_nonexistent_task(self, client):
        """DELETE on nonexistent task should return 404."""
        res = client.delete('/api/tasks/99999')
        assert res.status_code == 404
