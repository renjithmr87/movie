# Deployment Guide

This guide provides step-by-step instructions for deploying the Movie Database application.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Kubernetes Deployment](#kubernetes-deployment)
4. [Production Considerations](#production-considerations)

## Local Development

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- pip and virtualenv

### Steps

1. **Clone and Setup**
   ```bash
   git clone https://github.com/renjithmr87/movie.git
   cd movie
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Setup Database**
   ```bash
   # Create PostgreSQL database
   createdb moviedb
   
   # Or using psql
   psql -U postgres
   CREATE DATABASE moviedb;
   CREATE USER movieuser WITH PASSWORD 'moviepass';
   GRANT ALL PRIVILEGES ON DATABASE moviedb TO movieuser;
   \q
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access Application**
   - Web: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - API: http://localhost:8000/api/movies/

## Docker Deployment

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Using Docker Compose (Recommended for Local)

1. **Build and Start**
   ```bash
   docker-compose up --build
   ```

2. **Create Superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

3. **Access Application**
   - Web: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - API: http://localhost:8000/api/movies/

4. **Stop Services**
   ```bash
   docker-compose down
   ```

5. **Clean Volumes (Optional)**
   ```bash
   docker-compose down -v
   ```

### Manual Docker Build

1. **Build Image**
   ```bash
   docker build -t renjithmr87/movie:latest .
   ```

2. **Run PostgreSQL**
   ```bash
   docker run -d \
     --name moviedb \
     -e POSTGRES_DB=moviedb \
     -e POSTGRES_USER=movieuser \
     -e POSTGRES_PASSWORD=moviepass \
     -v postgres_data:/var/lib/postgresql/data \
     -p 5432:5432 \
     postgres:15-alpine
   ```

3. **Run Application**
   ```bash
   docker run -d \
     --name movie-app \
     --link moviedb:db \
     -e DB_HOST=db \
     -e DB_NAME=moviedb \
     -e DB_USER=movieuser \
     -e DB_PASSWORD=moviepass \
     -p 8000:8000 \
     renjithmr87/movie:latest
   ```

4. **Run Migrations**
   ```bash
   docker exec movie-app python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   docker exec -it movie-app python manage.py createsuperuser
   ```

## Kubernetes Deployment

### Prerequisites
- KIND (Kubernetes in Docker) or any Kubernetes cluster
- kubectl CLI tool
- Docker

### KIND Cluster Setup

1. **Install KIND**
   ```bash
   # On Linux
   curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
   chmod +x ./kind
   sudo mv ./kind /usr/local/bin/kind
   ```

2. **Create Cluster**
   ```bash
   kind create cluster --name movie-cluster
   ```

3. **Verify Cluster**
   ```bash
   kubectl cluster-info --context kind-movie-cluster
   kubectl get nodes
   ```

### Deploy to Kubernetes

1. **Build and Push Image**
   ```bash
   # Build
   docker build -t renjithmr87/movie:latest .
   
   # Login to DockerHub
   docker login
   
   # Push
   docker push renjithmr87/movie:latest
   ```

2. **Apply Kubernetes Manifests**
   ```bash
   # Create namespace
   kubectl apply -f k8s/namespace.yaml
   
   # Create ConfigMap and Secret
   kubectl apply -f k8s/configmap.yaml
   kubectl apply -f k8s/secret.yaml
   
   # Create Persistent Volume
   kubectl apply -f k8s/postgres-pv.yaml
   
   # Deploy PostgreSQL
   kubectl apply -f k8s/postgres-deployment.yaml
   
   # Wait for PostgreSQL to be ready
   kubectl wait --for=condition=ready pod -l app=postgres -n movie-app --timeout=120s
   
   # Deploy Application
   kubectl apply -f k8s/movie-deployment.yaml
   ```

3. **Verify Deployment**
   ```bash
   # Check all resources
   kubectl get all -n movie-app
   
   # Check pods
   kubectl get pods -n movie-app -w
   
   # Check logs
   kubectl logs -n movie-app -l app=movie-app
   ```

4. **Access Application**
   ```bash
   # Port forward
   kubectl port-forward -n movie-app service/movie-service 8000:80
   
   # Access at http://localhost:8000
   ```

5. **Create Superuser in K8s**
   ```bash
   # Get pod name
   POD_NAME=$(kubectl get pods -n movie-app -l app=movie-app -o jsonpath='{.items[0].metadata.name}')
   
   # Create superuser
   kubectl exec -it -n movie-app $POD_NAME -- python manage.py createsuperuser
   ```

### Update Deployment

1. **Update Image**
   ```bash
   # Build and push new image
   docker build -t renjithmr87/movie:v2 .
   docker push renjithmr87/movie:v2
   
   # Update deployment
   kubectl set image deployment/movie-app -n movie-app movie-app=renjithmr87/movie:v2
   
   # Or restart deployment
   kubectl rollout restart deployment/movie-app -n movie-app
   ```

2. **Check Rollout Status**
   ```bash
   kubectl rollout status deployment/movie-app -n movie-app
   ```

### Troubleshooting K8s

1. **Pod Not Starting**
   ```bash
   kubectl describe pod -n movie-app <pod-name>
   kubectl logs -n movie-app <pod-name>
   ```

2. **Database Connection Issues**
   ```bash
   # Check PostgreSQL pod
   kubectl get pods -n movie-app -l app=postgres
   kubectl logs -n movie-app -l app=postgres
   
   # Test connection from app pod
   kubectl exec -it -n movie-app <app-pod-name> -- sh
   nc -zv postgres-service 5432
   ```

3. **ConfigMap/Secret Issues**
   ```bash
   kubectl get configmap -n movie-app movie-config -o yaml
   kubectl get secret -n movie-app movie-secrets -o yaml
   ```

4. **Service Not Accessible**
   ```bash
   kubectl get svc -n movie-app
   kubectl describe svc -n movie-app movie-service
   ```

### Clean Up K8s

```bash
# Delete all resources
kubectl delete namespace movie-app

# Delete KIND cluster
kind delete cluster --name movie-cluster
```

## Production Considerations

### Security

1. **Environment Variables**
   - Generate a strong `SECRET_KEY`
   - Set `DEBUG=False`
   - Configure proper `ALLOWED_HOSTS`
   - Use strong database passwords

2. **Kubernetes Secrets**
   ```bash
   # Create secret from literal values
   kubectl create secret generic movie-secrets \
     --from-literal=SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())') \
     --from-literal=DB_PASSWORD=your-strong-password \
     -n movie-app
   ```

3. **SSL/TLS**
   - Use Ingress with TLS
   - Configure cert-manager for automatic certificates

### Performance

1. **Database**
   - Use connection pooling
   - Configure proper indexes
   - Regular backups

2. **Application**
   - Scale horizontally (increase replicas)
   - Use caching (Redis)
   - Configure CDN for static files

3. **Resource Limits**
   ```yaml
   resources:
     requests:
       memory: "256Mi"
       cpu: "250m"
     limits:
       memory: "1Gi"
       cpu: "1000m"
   ```

### Monitoring

1. **Logs**
   ```bash
   # Stream logs
   kubectl logs -f -n movie-app -l app=movie-app
   
   # Logs from all pods
   kubectl logs -n movie-app -l app=movie-app --all-containers=true
   ```

2. **Metrics**
   - Install Prometheus and Grafana
   - Configure Django to expose metrics
   - Monitor database performance

### Backup and Restore

1. **Database Backup**
   ```bash
   # Backup
   kubectl exec -n movie-app -l app=postgres -- pg_dump -U movieuser moviedb > backup.sql
   
   # Restore
   kubectl exec -i -n movie-app -l app=postgres -- psql -U movieuser moviedb < backup.sql
   ```

2. **Application State**
   - Version control for code
   - Document configuration changes
   - Regular testing of restore procedures

### High Availability

1. **Multiple Replicas**
   - Run at least 2 replicas of the app
   - Configure PodDisruptionBudget
   - Use anti-affinity rules

2. **Database HA**
   - Consider PostgreSQL cluster (Patroni, Stolon)
   - Configure replication
   - Regular backups

## CI/CD with GitHub Actions

The project includes automated CI/CD:

1. **Required Secrets**
   - Go to GitHub repo → Settings → Secrets
   - Add `DOCKER_USERNAME`
   - Add `DOCKER_PASSWORD`

2. **Workflow Triggers**
   - Automatic on push to `main` or `develop`
   - Automatic on pull requests

3. **Pipeline Stages**
   - Run tests
   - Build Docker image
   - Push to DockerHub

4. **Manual Deployment**
   - Pull latest image in K8s
   - Update deployment
   - Verify rollout

## Support

For issues or questions:
- Check logs: `kubectl logs -n movie-app <pod-name>`
- Check events: `kubectl get events -n movie-app`
- Check pod status: `kubectl describe pod -n movie-app <pod-name>`
- Review documentation: README.md
