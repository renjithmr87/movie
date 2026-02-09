#!/bin/bash
# Setup Movie App with Docker Compose

set -e

echo "=========================================="
echo "Movie App Docker Compose Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}docker-compose is not installed.${NC}"
    echo "Please install docker-compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}.env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}.env file created. Please review and update if needed.${NC}"
fi

# Build and start services
echo -e "${GREEN}Building and starting services...${NC}"
docker-compose up --build -d

# Wait for services to be healthy
echo -e "${YELLOW}Waiting for services to be healthy...${NC}"
sleep 10

# Check service status
echo -e "${GREEN}Service Status:${NC}"
docker-compose ps

# Check if database is ready
echo -e "${YELLOW}Checking database connection...${NC}"
for i in {1..30}; do
    if docker-compose exec -T db pg_isready -U movieuser -d moviedb &> /dev/null; then
        echo -e "${GREEN}Database is ready!${NC}"
        break
    fi
    echo "Waiting for database... ($i/30)"
    sleep 2
done

# Run migrations
echo -e "${GREEN}Running database migrations...${NC}"
docker-compose exec -T web python manage.py migrate

# Collect static files
echo -e "${GREEN}Collecting static files...${NC}"
docker-compose exec -T web python manage.py collectstatic --noinput

echo ""
echo -e "${GREEN}=========================================="
echo "Setup Complete!"
echo -e "==========================================${NC}"
echo ""
echo "Application is running at: http://localhost:8000"
echo ""
echo "To create a superuser, run:"
echo -e "${YELLOW}docker-compose exec web python manage.py createsuperuser${NC}"
echo ""
echo "To view logs:"
echo -e "${YELLOW}docker-compose logs -f${NC}"
echo ""
echo "To stop services:"
echo -e "${YELLOW}docker-compose down${NC}"
echo ""
echo "To stop and remove volumes:"
echo -e "${YELLOW}docker-compose down -v${NC}"
echo ""
exit 0
