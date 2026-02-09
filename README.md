# Movie Database Application

A Django application with PostgreSQL for managing movies, featuring CRUD operations and deployment on Kubernetes (KIND) cluster with GitOps CI/CD.

## 🎯 Project Overview

This project demonstrates a complete full-stack application with:
- Django web framework with REST API
- PostgreSQL database
- Docker containerization
- Kubernetes deployment
- CI/CD pipeline with GitHub Actions
- GitOps workflow

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         GitHub Actions CI/CD            │
│  (Build, Test, Push to DockerHub)      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│          DockerHub Registry             │
│      (renjithmr87/movie:latest)         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Kubernetes (KIND) Cluster          │
│  ┌───────────────────────────────────┐  │
│  │   Movie App Deployment (2 pods)   │  │
│  │   - Django Application            │  │
│  │   - Gunicorn WSGI Server          │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │   PostgreSQL Deployment           │  │
│  │   - Persistent Volume             │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Kubernetes (KIND) cluster
- kubectl CLI
- Git
- 4GB RAM (minimum)

## 🚀 Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/renjithmr87/movie.git
cd movie
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Run with Docker Compose (Recommended)

```bash
docker-compose up --build
```

The application will be available at:
- Web Interface: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- REST API: http://localhost:8000/api/movies/

### 6. Manual Setup (Without Docker)

```bash
# Start PostgreSQL (ensure it's running on localhost:5432)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

## 🎬 CRUD Operations

### Web Interface

1. **Create**: Navigate to `/create/` or click "Add New Movie"
2. **Read**: View all movies at `/` or individual movie at `/<id>/`
3. **Update**: Click "Edit" on any movie or navigate to `/<id>/update/`
4. **Delete**: Click "Delete" on any movie or navigate to `/<id>/delete/`

### REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/movies/` | List all movies |
| POST | `/api/movies/` | Create a new movie |
| GET | `/api/movies/{id}/` | Retrieve a movie |
| PUT | `/api/movies/{id}/` | Update a movie |
| PATCH | `/api/movies/{id}/` | Partial update |
| DELETE | `/api/movies/{id}/` | Delete a movie |

### Example API Requests

```bash
# List all movies
curl http://localhost:8000/api/movies/

# Create a new movie
curl -X POST http://localhost:8000/api/movies/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Shawshank Redemption",
    "director": "Frank Darabont",
    "genre": "Drama",
    "year": 1994,
    "rating": 9.3,
    "duration": 142,
    "description": "Two imprisoned men bond over years..."
  }'

# Get a specific movie
curl http://localhost:8000/api/movies/1/

# Update a movie
curl -X PUT http://localhost:8000/api/movies/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Shawshank Redemption",
    "director": "Frank Darabont",
    "genre": "Drama",
    "year": 1994,
    "rating": 9.5,
    "duration": 142,
    "description": "Updated description..."
  }'

# Delete a movie
curl -X DELETE http://localhost:8000/api/movies/1/
```

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t renjithmr87/movie:latest .
```

### Push to DockerHub

```bash
docker login
docker push renjithmr87/movie:latest
```

## ☸️ Kubernetes Deployment (KIND)

### 1. Create KIND Cluster

```bash
kind create cluster --name movie-cluster
```

### 2. Apply Kubernetes Manifests

```bash
# Apply in order
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/postgres-pv.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/movie-deployment.yaml
```

### 3. Verify Deployment

```bash
# Check all resources
kubectl get all -n movie-app

# Check pods status
kubectl get pods -n movie-app

# Check services
kubectl get svc -n movie-app

# View logs
kubectl logs -n movie-app deployment/movie-app
```

### 4. Access the Application

```bash
# Port forward to access locally
kubectl port-forward -n movie-app service/movie-service 8000:80

# Access at http://localhost:8000
```

### 5. Create Django Superuser in K8s

```bash
kubectl exec -it -n movie-app deployment/movie-app -- python manage.py createsuperuser
```

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for automated CI/CD:

### Workflow Triggers
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

### Pipeline Stages

1. **Test Stage**
   - Sets up Python environment
   - Installs dependencies
   - Runs database migrations
   - Executes tests

2. **Build and Push Stage** (only on push to main/develop)
   - Builds Docker image
   - Pushes to DockerHub
   - Tags with branch name and SHA

### Required GitHub Secrets

Add these secrets to your GitHub repository:
- `DOCKER_USERNAME`: Your DockerHub username
- `DOCKER_PASSWORD`: Your DockerHub password/token

## 📁 Project Structure

```
movie/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # CI/CD pipeline
├── k8s/                        # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── postgres-pv.yaml
│   ├── postgres-deployment.yaml
│   └── movie-deployment.yaml
├── movieproject/               # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── movies/                     # Django app
│   ├── models.py              # Movie model
│   ├── views.py               # CRUD views
│   ├── serializers.py         # DRF serializers
│   ├── urls.py                # URL routing
│   ├── admin.py               # Admin configuration
│   └── templates/             # HTML templates
│       └── movies/
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Local development setup
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | (generated) |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hosts | `*` |
| `DB_NAME` | Database name | `moviedb` |
| `DB_USER` | Database user | `movieuser` |
| `DB_PASSWORD` | Database password | `moviepass` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run tests with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📊 Resource Requirements

### Minimum System Requirements
- **RAM**: 4GB
- **CPU**: 2 cores
- **Disk**: 10GB free space

### Kubernetes Resource Allocation
- **PostgreSQL**: 256Mi-512Mi RAM, 250m-500m CPU
- **Django App**: 256Mi-512Mi RAM per pod, 250m-500m CPU
- **Replicas**: 2 pods for high availability

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check PostgreSQL is running
   docker-compose ps
   # Check environment variables
   echo $DB_HOST $DB_PORT
   ```

2. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Kubernetes Pod Not Starting**
   ```bash
   kubectl describe pod -n movie-app <pod-name>
   kubectl logs -n movie-app <pod-name>
   ```

4. **Migration Issues**
   ```bash
   python manage.py showmigrations
   python manage.py migrate --fake-initial
   ```

## 🔐 Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use strong database passwords
- Configure proper `ALLOWED_HOSTS`
- Keep dependencies updated
- Use secrets management in Kubernetes

## 📚 Technology Stack

- **Backend**: Django 4.2.26
- **Database**: PostgreSQL 15
- **API**: Django REST Framework 3.14.0
- **WSGI Server**: Gunicorn 22.0.0
- **Containerization**: Docker
- **Orchestration**: Kubernetes (KIND)
- **CI/CD**: GitHub Actions
- **Static Files**: WhiteNoise

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is open-source and available for practice and learning purposes.

## 👤 Author

**renjithmr87**
- GitHub: [@renjithmr87](https://github.com/renjithmr87)
- DockerHub: [renjithmr87](https://hub.docker.com/u/renjithmr87)

## 🙏 Acknowledgments

- Django Documentation
- Kubernetes Documentation
- Docker Documentation
- PostgreSQL Community

