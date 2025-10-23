# Todo App - Kubernetes GitOps Deployment

A simple Flask-based todo application deployed to Kubernetes using GitOps principles with ArgoCD.

## About

This project demonstrates a complete DevOps workflow for deploying a web application to Kubernetes. It includes containerization with Docker, infrastructure as code with Terraform, and automated deployment using ArgoCD.

## Features

- ✅ Add, complete, and delete tasks
- ✅ Clean and responsive UI
- ✅ SQLite database for persistence
- ✅ Containerized with Docker
- ✅ Kubernetes deployment manifests
- ✅ GitOps workflow with ArgoCD
- ✅ Infrastructure as Code with Terraform

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS
- **Container**: Docker
- **Orchestration**: Kubernetes
- **GitOps**: ArgoCD
- **IaC**: Terraform (Azure)

## Project Structure

```
todo-app/
├── app.py                  # Flask application
├── schema.sql             # Database schema
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container image definition
├── templates/            # HTML templates
│   └── index.html
├── static/              # CSS and static files
│   └── style.css
├── k8s/                 # Kubernetes manifests
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── argocd-application.yaml
└── Iac/                 # Terraform files
    ├── main.tf
    └── variables.tf
```

## Quick Start

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit `http://localhost:5000` to use the app.

### Running with Docker

```bash
# Build the image
docker build -t todo-app .

# Run the container
docker run -p 5000:5000 todo-app
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (minikube, AKS, EKS, or GKE)
- kubectl configured
- ArgoCD installed on the cluster

### Manual Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check deployment status
kubectl get pods -n todo-app
kubectl get svc -n todo-app
```

### GitOps Deployment with ArgoCD

1. **Install ArgoCD**

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

2. **Access ArgoCD UI**

```bash
# Port forward
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

3. **Deploy the Application**

```bash
kubectl apply -f k8s/argocd-application.yaml
```

ArgoCD will automatically sync and deploy your application from the GitHub repository.

## Docker Image

The application is available on Docker Hub:

```
docker pull tuheen27/gitops:latest
```

## Infrastructure Deployment

The project includes Terraform configurations for deploying to Azure Kubernetes Service (AKS).

```bash
cd Iac

# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Apply infrastructure
terraform apply
```

This will create:
- Azure Resource Group
- Azure Kubernetes Service (AKS)
- Azure Container Registry (ACR)
- Role assignments for pulling images

## Configuration

### Environment Variables

- `DATABASE`: Path to SQLite database file (default: `todo.db`)

### Kubernetes Resources

- **Namespace**: `todo-app`
- **Replicas**: 2 pods
- **Service Type**: LoadBalancer
- **Port**: 80 → 5000

## Development

### Adding New Features

1. Make changes to `app.py` or templates
2. Test locally
3. Build and push new Docker image
4. Commit and push to GitHub
5. ArgoCD automatically syncs the changes

### Database Schema

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT 0
);
```

## Monitoring

```bash
# View logs
kubectl logs -n todo-app -l app=todo-app -f

# Check pod status
kubectl get pods -n todo-app

# Describe deployment
kubectl describe deployment -n todo-app
```

## Troubleshooting

### Pods not starting

```bash
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
```

### Service not accessible

```bash
kubectl get svc -n todo-app
kubectl describe svc todo-app-service -n todo-app
```

### ArgoCD sync issues

```bash
kubectl get application -n argocd
kubectl describe application todo-app -n argocd
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - feel free to use this project for learning and development.

## Author

Tuheen - [GitHub](https://github.com/tuheen27)

## Acknowledgments

- Built with Flask and love ❤️
- Deployed with Kubernetes and ArgoCD
- Inspired by DevOps best practices
