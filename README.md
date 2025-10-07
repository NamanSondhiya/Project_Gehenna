# Gehenna - 3-Tier Flask Application

A production-ready 3-tier web application built with Flask, MongoDB, and deployed on Amazon EKS using DevSecOps best practices.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Frontend      │    │   Backend       │    │   Database      │
│   (Flask)       │◄──►│   (Flask API)   │◄──►│   (MongoDB)     │
│   Port: 8001    │    │   Port: 8002    │    │   Port: 27017   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │                 │
                    │  Mongo Express  │
                    │  (Admin UI)     │
                    │  Port: 8081     │
                    │                 │
                    └─────────────────┘
```

**[Screenshot Placeholder: Local Architecture Diagram]**

**[Screenshot Placeholder: Kubernetes Architecture Diagram]**

This application follows a 3-tier architecture:
- **Frontend**: Flask web application serving the user interface
- **Backend**: Flask REST API handling business logic
- **Database**: MongoDB for data persistence
- **Admin Interface**: Mongo Express for database management

### Kubernetes Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Amazon EKS Cluster                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   gehenna namespace                     │    │
│  │                                                         │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │    │
│  │  │  Frontend   │    │   Backend   │    │  Database   │  │    │
│  │  │    Pod      │◄──►│     Pod     │◄──►│     Pod     │  │    │
│  │  │             │    │             │    │             │  │    │
│  │  └─────────────┘    └─────────────┘    └─────────────┘  │    │
│  │         │                   │                   │       │    │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │    │
│  │  │  Frontend   │    │   Backend   │    │   MongoDB   │  │    │
│  │  │   Service   │    │   Service   │    │   Service   │  │    │
│  │  │ (ClusterIP) │    │ (ClusterIP) │    │ (ClusterIP) │  │    │
│  │  └─────────────┘    └─────────────┘    └─────────────┘  │    │
│  │                                                         │    │
│  │  ┌─────────────┐                                        │    │
│  │  │Mongo Express│                                        │    │
│  │  │    Pod      │                                        │    │
│  │  │             │                                        │    │
│  │  └─────────────┘                                        │    │
│  │         │                                               │    │
│  │  ┌─────────────┐                                        │    │
│  │  │Mongo Express│                                        │    │
│  │  │   Service   │                                        │    │
│  │  │ (ClusterIP) │                                        │    │
│  │  └─────────────┘                                        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                 ConfigMaps & Secrets                    │    │
│  │  • Environment Variables                                │    │
│  │  • Database Credentials                                 │    │
│  │  • Service Configuration                                │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

**Key Kubernetes Components:**
- **Pods**: Containerized application instances
- **Services**: Internal load balancing and service discovery
- **ConfigMaps**: Environment configuration
- **Secrets**: Sensitive data like database credentials
- **Namespace**: Isolated environment (`gehenna`)
- **Helm Chart**: Package management for deployment

## 🚀 Features

- **Name Management System**: Add, delete, search, and view names
- **RESTful API**: Clean API endpoints with proper error handling
- **Input Validation**: Comprehensive validation and sanitization
- **Health Checks**: Built-in health monitoring endpoints
- **CORS Support**: Configurable cross-origin resource sharing
- **Logging**: Structured logging throughout the application

## 🛠️ Technology Stack

- **Frontend**: Flask, HTML, CSS, JavaScript
- **Backend**: Flask, Python
- **Database**: MongoDB
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Amazon EKS)
- **Package Management**: Helm Charts
- **CI/CD**: Jenkins with Shared Libraries
- **GitOps**: ArgoCD
- **Monitoring**: Kube-Prometheus-Stack
- **Security**: OWASP Dependency Check, Trivy, SonarQube

## 📁 Project Structure

```
gehenna_2.0/
├── backend/                 # Backend Flask API
│   ├── app.py              # Main application
│   ├── connection.py       # Database connection
│   ├── Dockerfile          # Backend container
│   └── requirements.txt    # Python dependencies
├── frontend/               # Frontend Flask app
│   ├── templates/          # HTML templates
│   ├── app.py             # Frontend application
│   ├── Dockerfile         # Frontend container
│   └── requirements.txt   # Python dependencies
├── kubernetes/            # Helm chart
│   ├── templates/         # K8s manifests
│   ├── Chart.yaml         # Helm chart metadata
│   └── values.yaml        # Configuration values
├── GitOps/               # GitOps configuration
│   └── Jenkinsfile       # CD pipeline
├── Jenkinsfile           # CI pipeline
├── docker-compose.yml    # Local development
└── sonar-project.properties # SonarQube config
```

## 🔧 Local Development

### Prerequisites
- Docker and Docker Compose
- Python 3.9+
- Node.js (for development tools)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/NamanSondhiya/Project_Gehenna.git
   cd Project_Gehenna
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost:8001
   - Backend API: http://localhost:8002
   - Mongo Express: http://localhost:8081

**[Screenshot Placeholder: Local Development Setup]**

## 🏭 Production Deployment

### Amazon EKS Deployment

**[Screenshot Placeholder: EKS Cluster Overview]**

The application is deployed on Amazon EKS using Helm charts with the following components:

#### Prerequisites
- Amazon EKS cluster
- kubectl configured
- Helm 3.x installed
- ArgoCD installed on cluster

#### Deployment Steps

1. **Deploy using Helm**
   ```bash
   helm install gehenna ./kubernetes -n gehenna --create-namespace
   ```

2. **Verify deployment**
   ```bash
   kubectl get pods -n gehenna
   kubectl get services -n gehenna
   ```

**[Screenshot Placeholder: Kubernetes Pods Status]**

**[Screenshot Placeholder: Kubernetes Services]**

## 🔄 CI/CD Pipeline

### Jenkins CI Pipeline

**[Screenshot Placeholder: Jenkins Pipeline Overview]**

The CI pipeline implements DevSecOps best practices with the following stages:

#### Pipeline Stages

1. **Parameter Validation**
   - Validates required image tags
   - Ensures proper input format

2. **Code Quality & Security**
   - **SonarQube Analysis**: Code quality and security scanning
   - **Quality Gate**: Enforces quality standards
   - **OWASP Dependency Check**: Identifies vulnerable dependencies
   - **Trivy Filesystem Scan**: Scans for secrets and vulnerabilities

**[Screenshot Placeholder: SonarQube Dashboard]**

**[Screenshot Placeholder: OWASP Dependency Check Results]**

3. **Build & Security Scanning**
   - **Parallel Docker Builds**: Frontend and backend images
   - **Trivy Image Scanning**: Container vulnerability assessment
   - **Multi-stage builds**: Optimized container images

**[Screenshot Placeholder: Trivy Scan Results]**

4. **Artifact Management**
   - **DockerHub Push**: Conditional image publishing
   - **Artifact Archiving**: Security reports and build artifacts
   - **Email Notifications**: Automated notifications for build success/failure with security reports attached
   - **CD Pipeline Trigger**: Automatically triggers GitOps deployment on successful CI build

**[Screenshot Placeholder: DockerHub Repository]**

#### Jenkins Shared Library Integration

The pipeline leverages custom Jenkins shared libraries from [jenkins-trusted-libraries](https://github.com/NamanSondhiya/Jenkins-trusted-libraries.git):
- `git_clone()`: Standardized Git operations
- `sonarqube_analysis()`: SonarQube integration
- `owasp_scan()`: OWASP dependency checking
- `trivy_fs_scan()` & `trivy_image_scan()`: Security scanning
- `docker_build()`, `docker_push()`: Container operations

**[Screenshot Placeholder: Jenkins Shared Library Usage]**

### ArgoCD GitOps

**[Screenshot Placeholder: ArgoCD Application Dashboard]**

Continuous Deployment is managed through ArgoCD with:
- **Automated Sync**: Git-based deployment triggers
- **Health Monitoring**: Application health status
- **Rollback Capabilities**: Easy rollback to previous versions
- **Email Notifications**: Build status notifications for both CI and CD pipelines


**[Screenshot Placeholder: ArgoCD Sync Status]**

**[Screenshot Placeholder: ArgoCD Application Health]**

## 📊 Monitoring & Observability

### Kube-Prometheus-Stack

**[Screenshot Placeholder: Grafana Dashboard Overview]**

Comprehensive monitoring setup includes:

#### Prometheus Metrics
- Application performance metrics
- Infrastructure monitoring
- Custom business metrics
- Alert rules and thresholds

**[Screenshot Placeholder: Prometheus Targets]**

#### Grafana Dashboards
- **Application Dashboard**: Request rates, response times, error rates
- **Infrastructure Dashboard**: CPU, memory, disk, network usage
- **Business Dashboard**: User activity, feature usage

**[Screenshot Placeholder: Application Metrics Dashboard]**

**[Screenshot Placeholder: Infrastructure Monitoring Dashboard]**



## 🔒 Security Features

### DevSecOps Implementation

**[Screenshot Placeholder: Security Scan Summary]**

- **Static Application Security Testing (SAST)**: SonarQube integration
- **Dependency Scanning**: OWASP Dependency Check
- **Container Security**: Trivy vulnerability scanning
- **Secrets Management**: Kubernetes secrets and environment variables
- **Network Policies**: Kubernetes network segmentation
- **RBAC**: Role-based access control

### Security Best Practices

- Input validation and sanitization
- CORS configuration
- Health check endpoints
- Secure container images
- Non-root container execution
- Resource limits and quotas



## 📈 Performance Metrics

**[Screenshot Placeholder: Performance Dashboard]**

Key performance indicators:
- **Response Time**: Average API response time
- **Throughput**: Requests per second
- **Error Rate**: Percentage of failed requests
- **Availability**: Uptime percentage
- **Resource Utilization**: CPU, memory, storage usage

## 🔧 Configuration

### Environment Variables

#### Frontend
- `BACKEND_URL`: Backend service URL
- `PORT`: Frontend service port
- `HOST`: Bind address

#### Backend
- `MONGO_URL`: MongoDB connection string
- `PORT`: Backend service port
- `HOST`: Bind address
- `FRONTEND_ORIGINS`: CORS allowed origins

### Kubernetes Configuration

The Helm chart supports customization through `values.yaml`:

```yaml
namespace: gehenna
frontendImage: docker.io/namanss/gehenna-frontend-ii:3.2
backendImage: docker.io/namanss/gehenna-backend-ii:3.2
mongoexpressImage: docker.io/mongo-express:1.0.2-20-alpine3.19
mongoImage: docker.io/mongo:noble
```

## 🧪 Testing

**[Screenshot Placeholder: Test Results]**

### API Testing
```bash
# Health check
curl http://localhost:8002/health

# Get all names
curl http://localhost:8002/api/get

# Add a name
curl -X POST http://localhost:8002/api/add/John

# Search names
curl http://localhost:8002/api/search/Jo
```

## 📝 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service status |
| GET | `/health` | Health check |
| GET | `/api/get` | Retrieve all names |
| POST | `/api/add/<name>` | Add a new name |
| DELETE | `/api/delete/<name>` | Delete a name |
| GET | `/api/search/<query>` | Search names |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run security scans locally
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Team

- **Developer**: Naman Sondhiya
- **Email**: ssnaman4@gmail.com

## 🔗 Links

- **GitHub Repository**: https://github.com/NamanSondhiya/Project_Gehenna
- **DockerHub**: https://hub.docker.com/u/namanss

---

**Note**: This README includes placeholder sections for screenshots. Please add relevant screenshots showing:
- Architecture diagrams
- Jenkins pipeline execution
- SonarQube analysis results
- Security scan reports
- Kubernetes deployment status
- ArgoCD application status
- Grafana monitoring dashboards
- Email notification examples

For any questions or support, please contact the development team.