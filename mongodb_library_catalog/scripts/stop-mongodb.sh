#!/bin/bash

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
