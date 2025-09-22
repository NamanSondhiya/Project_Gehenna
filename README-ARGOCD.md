# ArgoCD Integration for Project Gehenna

This document describes how to integrate Project Gehenna with ArgoCD for GitOps-based deployments.

## Repository Structure

```
gehenna/
├── backend/              # Backend application code
├── frontend/             # Frontend application code
├── k8s/                  # Kubernetes manifests
│   ├── backend.yaml
│   ├── frontend.yaml
│   ├── mongo-express.yaml
│   └── mongo.yaml
└── argocd/               # ArgoCD configuration
    └── gehenna-app.yaml  # ArgoCD Application manifest
```

## Integration Steps

### 1. Create ArgoCD Application Manifest

Create a file in the argocd directory:

```bash
mkdir -p argocd
```

Create the ArgoCD application manifest:

```bash
cat > argocd/gehenna-app.yaml << EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: gehenna
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/SillyCookies-s/Project-Gehenna.git
    targetRevision: main
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: gehenna
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
EOF
```

This manifest tells ArgoCD to:
- Monitor the `k8s` directory in your GitHub repository
- Deploy all Kubernetes resources to the `gehenna` namespace
- Automatically sync changes when they're pushed to the repository

### 2. Apply the ArgoCD Application Manifest

```bash
kubectl apply -f argocd/gehenna-app.yaml
```

### 3. Access the ArgoCD UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Open your browser and navigate to https://localhost:8080

Login with the default credentials:
- Username: admin
- Password: (retrieve with the command below)

```bash
kubectl -n argocd get secret argocd-initial-admin-password -o jsonpath="{.data.password}" | base64 -d
```

## Deployment Process

1. Changes are pushed to the Git repository
2. ArgoCD detects changes in the repository
3. ArgoCD applies the changes to the Kubernetes cluster
4. The application is updated automatically

## Manual Sync

If needed, you can manually sync the application in the ArgoCD UI or using the ArgoCD CLI:

```bash
argocd app sync gehenna
```

## Quick Start Guide

1. Ensure ArgoCD is installed in your Kubernetes cluster in the `argocd` namespace
2. Apply the ArgoCD application manifest:
   ```bash
   kubectl apply -f argocd/gehenna-app.yaml
   ```
3. Access the ArgoCD UI and verify that the application is syncing
4. Make changes to your Kubernetes manifests in the `k8s` directory
5. Push changes to GitHub
6. ArgoCD will automatically detect and apply the changes

## Troubleshooting

- **Application not syncing**: Check the ArgoCD logs with `kubectl logs -n argocd deployment/argocd-application-controller`
- **Application showing errors**: Check the application events in the ArgoCD UI or with `kubectl describe application gehenna -n argocd`
- **Connection issues**: Ensure ArgoCD has access to your GitHub repository
- **Resources not being created**: Check if the namespace exists with `kubectl get ns gehenna`