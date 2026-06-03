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
# On Linux/Mac/Git Bash:
kill -9 <PID>
# On Windows PowerShell:
Stop-Process -Id <PID> -Force
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

1. Forward port to access Prometheus:
   ```bash
   kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090
   ```
2. Open Prometheus UI: http://localhost:9090
3. Go to **Status → Targets**
4. Check if the target matching our Flask app (port 5000) shows `UP`.
5. If missing, verify that the application pod has the scraping annotations configured:
   ```bash
   kubectl get pods -n devops101 -o yaml
   ```

---

### Grafana Can't See Data

1. Forward port to access Grafana:
   ```bash
   kubectl port-forward svc/prometheus-grafana -n monitoring 3000:80
   ```
2. Open Grafana: http://localhost:3000
3. Go to **Connections → Data Sources → Prometheus** and click **Save & test** to verify the connection is active.
4. Check Grafana pod logs if you experience connection errors:
   ```bash
   kubectl logs -l app.kubernetes.io/name=grafana -n monitoring -c grafana
   ```

---

## 🔑 Grafana Credentials & Password Reset

### Setting a custom password (recommended)
You can configure a custom admin password during installation or upgrade using `--set`:
```bash
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring \
  --create-namespace \
  --set grafana.adminPassword="your-secure-password"
```

### Resetting the password for a running Pod
If the pod is running, you can reset the password directly inside the Grafana container:
```bash
kubectl exec -it deploy/prometheus-grafana -n monitoring -c grafana -- grafana cli admin reset-admin-password newpassword
```


---

## 🧹 Full Clean Reset

```bash
# Clean up Kubernetes resources
kubectl delete namespace devops101
helm uninstall prometheus -n monitoring
helm uninstall argocd -n argocd

# Clean up Docker (if testing local app container)
docker compose down
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

**On Linux/Mac/Git Bash:**
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

**On Windows PowerShell:**
```powershell
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}")))
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
