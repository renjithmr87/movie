#!/bin/bash
# Deploy Movie App to KIND Cluster

set -e

echo "=========================================="
echo "Movie App Kubernetes Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if KIND is installed
if ! command -v kind &> /dev/null; then
    echo -e "${RED}KIND is not installed. Please install KIND first.${NC}"
    echo "Visit: https://kind.sigs.k8s.io/docs/user/quick-start/"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}kubectl is not installed. Please install kubectl first.${NC}"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

CLUSTER_NAME="movie-cluster"

# Check if cluster already exists
if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    echo -e "${YELLOW}Cluster '${CLUSTER_NAME}' already exists.${NC}"
    read -p "Do you want to delete and recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Deleting existing cluster..."
        kind delete cluster --name ${CLUSTER_NAME}
    else
        echo "Using existing cluster..."
    fi
fi

# Create KIND cluster if it doesn't exist
if ! kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    echo -e "${GREEN}Creating KIND cluster: ${CLUSTER_NAME}${NC}"
    kind create cluster --name ${CLUSTER_NAME}
fi

# Set kubectl context
echo -e "${GREEN}Setting kubectl context...${NC}"
kubectl cluster-info --context kind-${CLUSTER_NAME}

# Apply Kubernetes manifests in order
echo -e "${GREEN}Applying Kubernetes manifests...${NC}"

echo "1. Creating namespace..."
kubectl apply -f k8s/namespace.yaml

echo "2. Creating ConfigMap..."
kubectl apply -f k8s/configmap.yaml

echo "3. Creating Secret..."
kubectl apply -f k8s/secret.yaml

echo "4. Creating Persistent Volume..."
kubectl apply -f k8s/postgres-pv.yaml

echo "5. Deploying PostgreSQL..."
kubectl apply -f k8s/postgres-deployment.yaml

echo "6. Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n movie-app --timeout=120s || {
    echo -e "${RED}PostgreSQL failed to start. Checking logs:${NC}"
    kubectl logs -n movie-app -l app=postgres --tail=50
    exit 1
}

echo "7. Deploying Movie Application..."
kubectl apply -f k8s/movie-deployment.yaml

echo "8. Waiting for Movie App to be ready..."
kubectl wait --for=condition=ready pod -l app=movie-app -n movie-app --timeout=180s || {
    echo -e "${YELLOW}Application might still be starting. Checking status:${NC}"
    kubectl get pods -n movie-app
    echo -e "${YELLOW}Checking logs:${NC}"
    kubectl logs -n movie-app -l app=movie-app --tail=50
}

echo ""
echo -e "${GREEN}=========================================="
echo "Deployment Status"
echo -e "==========================================${NC}"
kubectl get all -n movie-app

echo ""
echo -e "${GREEN}=========================================="
echo "Access Instructions"
echo -e "==========================================${NC}"
echo ""
echo "To access the application, run:"
echo -e "${YELLOW}kubectl port-forward -n movie-app service/movie-service 8000:80${NC}"
echo ""
echo "Then open: http://localhost:8000"
echo ""
echo "To create a superuser:"
echo -e "${YELLOW}POD_NAME=\$(kubectl get pods -n movie-app -l app=movie-app -o jsonpath='{.items[0].metadata.name}')${NC}"
echo -e "${YELLOW}kubectl exec -it -n movie-app \$POD_NAME -- python manage.py createsuperuser${NC}"
echo ""
echo "To check logs:"
echo -e "${YELLOW}kubectl logs -f -n movie-app -l app=movie-app${NC}"
echo ""
echo -e "${GREEN}Deployment completed successfully!${NC}"
