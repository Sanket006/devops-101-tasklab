# Kubernetes Deployment Guide

This guide describes how to deploy the Task Manager application to a Kubernetes cluster, configure local environments like Kind or Minikube, and manage resources using GitOps (Argo CD).

## 1. Setting Up a Local Cluster

Choose one of the following methods to spin up a local Kubernetes cluster.

### Method A: Using Kind (Recommended)
Kind (Kubernetes in Docker) allows running Kubernetes clusters using Docker container "nodes".

1. **Create the cluster:**
   We use a custom configuration [kind-config.yaml](file:///c:/Users/Lenovo/Sanket%20Personal/simple-devops-project/kind/kind-config.yaml) to map NodePort `30080` from the container node to your local host:
   ```bash
   kind create cluster --config kind/kind-config.yaml --name devops101
   ```

2. **Verify Node Status:**
   ```bash
   kubectl get nodes
   ```

### Method B: Using Minikube
Minikube runs a single-node Kubernetes cluster inside a virtual machine or container.

1. **Start Minikube:**
   ```bash
   minikube start
   ```

---

## 2. Deploying the Application Manifests

Our Kubernetes manifests are organized inside the `k8s/` directory.

> 📖 **Quick Concept Explanations:**
> * **Namespace:** Think of this as a virtual folder or project boundary. Deploys inside the `devops101` namespace are isolated from other applications in the cluster.
> * **NodePort Service:** Exposes a service on a specific port of the host node. This is a simple way to access your cluster web application from your host browser locally.

1. **Open and update `k8s/deployment.yaml`:**
   Locate the container image line and replace `sanket006` with your Docker Hub username:
   ```yaml
   image: YOUR_DOCKERHUB_USERNAME/devops101-app:sha-b9094ea
   ```

2. **Apply all manifests in the `k8s/` folder:**
   ```bash
   kubectl apply -f k8s/
   ```

3. **Monitor the rollouts:**
   Check the status of the namespace creation, configmap, services, deployments, and pods:
   ```bash
   kubectl get all -n devops101
   ```

4. **Wait for Pods to be Ready:**
   ```bash
   kubectl wait --for=condition=ready pod -l app=devops101 -n devops101 --timeout=60s
   ```

5. **Access the Web App:**
   * **On Kind:** Open your web browser and visit **[http://localhost:30080](http://localhost:30080)**.
   * **On Minikube:** Access the NodePort service dynamically by running:
     ```bash
     minikube service devops101-nodeport -n devops101
     ```

---

## 3. GitOps Synchronization with Argo CD

Instead of manual `kubectl apply` commands, you can set up Argo CD to synchronize your Git repository directly with the cluster.

### Step 1: Install Argo CD via Helm
Add the official repository and install the chart into the `argocd` namespace:
```bash
# Add Helm repo
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# Install Argo CD
helm install argocd argo/argo-cd --namespace argocd --create-namespace
```

### Step 2: Configure the GitOps Application
To register your repository directly in the cluster, replace `YOUR_GITHUB_USERNAME` in the block below, copy the command, and run it in your terminal:

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
    repoURL: 'https://github.com/YOUR_GITHUB_USERNAME/simple-devops-project.git'
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

### Step 3: Access the Argo CD UI
1. **Port-forward the Argo CD server:**
   ```bash
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```
2. Open **[http://localhost:8080](http://localhost:8080)** in your browser.
3. Login using the username `admin` and retrieve the password:
   * **On PowerShell:**
     ```powershell
     [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}")))
     ```
   * **On Bash/Zsh:**
     ```bash
     kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode
     ```

---

## 4. Troubleshooting & Useful Kubectl Commands

```bash
# Watch the pod creation or status changes
kubectl get pods -n devops101 -w

# Stream container logs for debugging
kubectl logs -l app=devops101 -n devops101 -f

# Inspect pod configuration, events, and health check failures
kubectl describe pod -l app=devops101 -n devops101

# Run interactive commands inside app pods
kubectl exec -it deployment/devops101-app -n devops101 -- bash

# Manually trigger a rolling update (e.g. reload settings)
kubectl rollout restart deployment devops101-app -n devops101

# Delete the namespace and cleanup all deployed resources
kubectl delete namespace devops101

# Completely delete the Kind cluster
kind delete cluster --name devops101

# Completely delete the Minikube cluster
minikube delete
```
