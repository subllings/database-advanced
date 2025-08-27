#!/bin/bash

# Navigate to project directory first: cd /e/_SoftEng/_BeCode/database-advanced/mongodb_library_catalog
# Make this file executable: chmod +x scripts/stop-mongodb.sh
# Run it with: ./scripts/stop-mongodb.sh
# chmod +x scripts/stop-mongodb.sh && ./scripts/stop-mongodb.sh

echo "Stopping MongoDB Library Catalog..."

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "Using 'docker compose' command..."
    DOCKER_COMPOSE="docker compose"
else
    echo "Using 'docker-compose' command..."
    DOCKER_COMPOSE="docker-compose"
fi

# Stop containers
echo "Stopping containers..."
$DOCKER_COMPOSE down

echo "MongoDB Library Catalog stopped."
echo ""
echo "To start again, run: ./scripts/start-mongodb.sh"
