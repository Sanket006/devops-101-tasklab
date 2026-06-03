# 🛠️ RUNBOOK — DevOps 101 Project
> Operational guide for running, debugging, and maintaining the project.

---

## 🟢 Start the Stack

```bash
docker compose up -d
```

Check all services are healthy:
```bash
docker compose ps
```

Expected output:
```
NAME                   STATUS         PORTS
devops101_app         Up (healthy)   0.0.0.0:5000->5000/tcp
devops101_prometheus  Up             0.0.0.0:9090->9090/tcp
devops101_grafana     Up             0.0.0.0:3000->3000/tcp
```

---

## 🔴 Stop the Stack

```bash
# Stop containers but keep data
docker compose stop

# Stop AND remove containers + networks
docker compose down

# Stop, remove containers, AND delete volumes (fresh slate)
docker compose down -v
```

---

## 🔁 Restart a Single Service

```bash
docker compose restart app
```

---

## 📋 View Logs

```bash
# All services
docker compose logs -f

# Just the app
docker compose logs -f app

# Last 50 lines
docker compose logs --tail=50 app
```

---

## 🩺 Verify Health Checks

```bash
# App health
curl http://localhost:5000/health

# App readiness
curl http://localhost:5000/ready

# Metrics
curl http://localhost:5000/metrics
```

---

## 🐛 Common Issues & Fixes

### Port Already in Use

**Error:** `Error starting userland proxy: listen tcp4 0.0.0.0:5000: bind: address already in use`

**Fix:**
```bash
# Find what's using port 5000
# On Windows:
netstat -ano | findstr :5000
# On Linux/Mac:
lsof -i :5000

# Kill the process
kill -9 <PID>
```

---

### App Container Not Starting

```bash
# Check the logs
docker compose logs app

# Check the container exit code
docker compose ps
```

---

### Image Build Fails

```bash
# Force a full rebuild (no cache)
docker compose build --no-cache app
docker compose up -d
```

---

### Prometheus Not Scraping App

1. Open Prometheus UI: http://localhost:9090
2. Go to **Status → Targets**
3. Check if `devops101-app` shows `UP`
4. If `DOWN`, check that app is running: `docker compose ps app`

---

### Grafana Can't See Data / Preloaded Dashboard Missing

1. Open Grafana: http://localhost:3000
2. Go to **Connections → Data Sources → Prometheus**
3. Click **Save & test** — should say "Data source connected and labels found"
4. If it fails, check that Prometheus is running: `docker compose ps prometheus`
5. If the dashboard is missing, check the **Dashboards** menu in the left sidebar under the "DevOps 101" folder.
6. If the dashboard is not present, check that the Grafana container logs show no provisioning errors:
   ```bash
   docker compose logs grafana
   ```

---

## 🔑 Grafana Credentials & Password Reset

### Setting a custom password (recommended)
You can configure a custom admin password before launching the stack by setting the `GRAFANA_ADMIN_PASSWORD` environment variable:
```bash
GRAFANA_ADMIN_PASSWORD="your-new-password" docker compose up -d
```

### Resetting the password for a running container
If the container is already running, you can reset the password directly using the Grafana CLI:
```bash
docker exec -it devops101_grafana grafana cli admin reset-admin-password newpassword
```

---

## 🧹 Full Clean Reset

```bash
# Remove everything including volumes (clean slate)
docker compose down -v
docker rmi devops101-app:local
docker compose up -d --build
```

---

## 📊 Useful Prometheus Queries

| Query | Description |
|---|---|
| `tasks_total` | Total tasks |
| `tasks_done_total` | Completed tasks |
| `tasks_pending_total` | Pending tasks |
| `up{job="devops101-app"}` | Is the app up? (1=yes, 0=no) |

---

## ☸️ Kubernetes Quick Commands

```bash
# See all resources in namespace
kubectl get all -n devops101

# Watch pods (live)
kubectl get pods -n devops101 -w

# App logs
kubectl logs -l app=devops101 -n devops101 -f

# Force restart pods
kubectl rollout restart deployment/devops101-app -n devops101

# Check rollout status
kubectl rollout status deployment/devops101-app -n devops101

# Roll back to previous version
kubectl rollout undo deployment/devops101-app -n devops101
```

---

## 🔄 GitOps Operations (Argo CD)

### Access the Argo CD UI
If you deployed Argo CD, you can access the dashboard by port-forwarding the API server:
```bash
# Port-forward the API server to http://localhost:8080
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Retrieve the default `admin` password:
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Sync status & CLI commands
If you install the Argo CD CLI, you can manage the application status directly:
```bash
# Log in to Argo CD server
argocd login localhost:8080

# Check application sync status
argocd app get devops101-app

# Manually trigger a synchronization
argocd app sync devops101-app
```
