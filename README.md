# Project Gehenna

A 3-tier application with Flask frontend, Flask backend, MongoDB database, and Mongo Express admin interface.

## Architecture

```
Frontend (Flask) → Backend (Flask) → MongoDB
                                   ↑
                     Mongo Express -+
```

## Components

- **Frontend**: Simple Flask web application that displays data from the backend
- **Backend**: Flask API that interacts with MongoDB
- **MongoDB**: NoSQL database storing application data
- **Mongo Express**: Web-based MongoDB admin interface

## Application Features

- Store and retrieve names in MongoDB
- View stored names through the frontend
- Add new names via the backend API
- Manage database through Mongo Express

## Setup Instructions

### Prerequisites

- Docker (for building images)
- Minikube (for local Kubernetes cluster)
- kubectl CLI tool

### Local Development

1. Pull the pre-built Docker images:
```bash
docker pull namanss/gehenna-frontend:latest
docker pull namanss/gehenna-backend:latest
```

Or build them locally:
```bash
cd frontend
docker build -t namanss/gehenna-frontend:latest .

cd ../backend
docker build -t namanss/gehenna-backend:latest .
```

2. For local development, deploy using Kubernetes

### Kubernetes Deployment with Minikube

1. Start Minikube:
```bash
minikube start
```

2. Create the namespace:
```bash
kubectl create namespace gehenna
```

3. Deploy all components at once:
```bash
kubectl apply -f k8s/
```

Or deploy components individually (better for understanding the process):
```bash
kubectl apply -f k8s/mongo.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
kubectl apply -f k8s/mongo-express.yaml
```

## Design Choices

1. **Port Configuration**: Application ports are configurable via environment variables in Kubernetes manifests, allowing deployment flexibility without code changes. Default ports (8001, 8002, 8081) can be overridden with custom ports (4000, 3000, 5000) as shown in the Kubernetes manifests.
2. **Docker Images**: Pre-built images are hosted on Docker Hub under the `namanss` profile.
3. **Namespace Approach**: Namespace is explicitly defined in Deployment resources but intentionally omitted from Service resources. Services will be created in the same namespace as the context in which the YAML files are applied (the gehenna namespace when following the setup instructions).

## Known Issues

1. **Error Handling**: Frontend lacks proper error handling for backend connection issues.

## API Endpoints

### Option 1: Port-forwarding (Recommended)

Use kubectl port-forward to access services locally:

```bash
# Frontend
kubectl port-forward -n gehenna svc/gehenna-frontend 4000:4000
# Access at http://localhost:4000

# Backend
kubectl port-forward -n gehenna svc/gehenna-backend 3000:3000
# Access at http://localhost:3000/api/get and http://localhost:3000/add/[name]

# Mongo Express
kubectl port-forward -n gehenna svc/mongo-express 5000:5000
# Access at http://localhost:5000
```

**Note**: Deploy all components in the correct order (MongoDB → Backend → Frontend) as each tier depends on the previous one. The frontend displays data from the backend, which in turn fetches data from MongoDB. No need to port-forward MongoDB directly as Mongo Express provides a web interface to view and manage the database.

### Option 2: Minikube Service

Alternatively, use minikube service to open services in browser:

```bash
minikube service gehenna-frontend -n gehenna
minikube service gehenna-backend -n gehenna
minikube service mongo-express -n gehenna
```

## Cloud Deployment

This application can be deployed to cloud Kubernetes services with minimal changes:

- **AWS EKS**: Use the same YAML files, but consider adding an AWS LoadBalancer service
- **Google GKE**: Use the same YAML files with GKE Ingress for external access
- **Azure AKS**: Use the same YAML files with Azure-specific storage classes

For production cloud deployments, consider:
- Using managed database services instead of containerized MongoDB
- Implementing proper secrets management
- Setting up CI/CD pipelines for automated deployment

## Improvements Needed

1. Add proper error handling
2. Implement proper health checks for services
3. Use Kubernetes secrets for credentials
4. Add persistent storage for MongoDB
5. Add resource limits and requests for containers

## Troubleshooting

- **Frontend shows no data**: Ensure backend is running and accessible
- **Backend connection errors**: Check MongoDB connection string and credentials
- **Mongo Express crash loop**: Verify MongoDB is running and credentials are correct