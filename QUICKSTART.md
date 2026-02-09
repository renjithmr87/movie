# Quick Start Guide

This guide helps you get the Movie Database application running quickly.

## Choose Your Method

### 1. Docker Compose (Easiest - Recommended)

Best for local development and testing.

```bash
# Clone the repository
git clone https://github.com/renjithmr87/movie.git
cd movie

# Run the automated setup script
./scripts/setup-docker.sh

# Or manually:
docker-compose up --build

# Create a superuser
docker-compose exec web python manage.py createsuperuser

# Access at http://localhost:8000
```

### 2. Kubernetes (KIND)

Best for practicing K8s deployment.

```bash
# Clone the repository
git clone https://github.com/renjithmr87/movie.git
cd movie

# Make sure KIND and kubectl are installed
# Run the automated deployment script
./scripts/deploy-k8s.sh

# Or manually:
kind create cluster --name movie-cluster
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/postgres-pv.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/movie-deployment.yaml

# Port forward to access
kubectl port-forward -n movie-app service/movie-service 8000:80

# Access at http://localhost:8000
```

### 3. Local Development

Best for making code changes.

```bash
# Clone the repository
git clone https://github.com/renjithmr87/movie.git
cd movie

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Make sure PostgreSQL is running
# Create database: createdb moviedb

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Access at http://localhost:8000
```

## First Steps After Setup

1. **Access the Application**
   - Web Interface: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin
   - REST API: http://localhost:8000/api/movies/

2. **Create Your First Movie**
   - Via Web: Click "Add New Movie"
   - Via API:
     ```bash
     curl -X POST http://localhost:8000/api/movies/ \
       -H "Content-Type: application/json" \
       -d '{
         "title": "The Matrix",
         "director": "Wachowski Brothers",
         "genre": "Sci-Fi",
         "year": 1999,
         "rating": 8.7,
         "duration": 136
       }'
     ```

3. **Test CRUD Operations**
   - Create: Add a new movie
   - Read: View movie list and details
   - Update: Edit an existing movie
   - Delete: Remove a movie

## Testing API Endpoints

```bash
# List all movies
curl http://localhost:8000/api/movies/

# Get a specific movie (replace 1 with actual ID)
curl http://localhost:8000/api/movies/1/

# Update a movie
curl -X PATCH http://localhost:8000/api/movies/1/ \
  -H "Content-Type: application/json" \
  -d '{"rating": 9.0}'

# Delete a movie
curl -X DELETE http://localhost:8000/api/movies/1/
```

## Troubleshooting

### Docker Issues

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Clean restart
docker-compose down -v
docker-compose up --build
```

### Kubernetes Issues

```bash
# Check pod status
kubectl get pods -n movie-app

# View logs
kubectl logs -n movie-app -l app=movie-app

# Describe pod for errors
kubectl describe pod -n movie-app <pod-name>

# Delete and recreate
kubectl delete namespace movie-app
./scripts/deploy-k8s.sh
```

### Database Connection Issues

**Docker Compose:**
```bash
# Check database is running
docker-compose exec db pg_isready -U movieuser

# Access database
docker-compose exec db psql -U movieuser -d moviedb
```

**Local:**
```bash
# Test connection
psql -U movieuser -d moviedb -h localhost

# Check .env file has correct credentials
cat .env
```

## Next Steps

- Read [README.md](README.md) for comprehensive documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment guides
- See [API.md](API.md) for complete API documentation
- Explore the code and make modifications
- Practice CI/CD by pushing changes to GitHub
- Deploy to a real Kubernetes cluster

## Common Commands

### Docker Compose

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f web

# Execute commands
docker-compose exec web python manage.py <command>

# Rebuild
docker-compose up --build
```

### Kubernetes

```bash
# View resources
kubectl get all -n movie-app

# View logs
kubectl logs -f -n movie-app -l app=movie-app

# Execute commands
kubectl exec -it -n movie-app <pod-name> -- python manage.py <command>

# Port forward
kubectl port-forward -n movie-app service/movie-service 8000:80

# Delete deployment
kubectl delete namespace movie-app
```

### Django Management

```bash
# Create superuser
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Shell
python manage.py shell
```

## Support

For more detailed information, refer to:
- [README.md](README.md) - Overview and setup
- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment instructions
- [API.md](API.md) - REST API documentation

Happy coding! 🎬
