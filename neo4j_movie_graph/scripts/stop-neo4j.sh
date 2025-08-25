#!/bin/bash

echo "Stopping Neo4j Movie Graph..."

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

echo "Neo4j Movie Graph stopped."
echo ""
echo "To start again, run: ./scripts/start-neo4j.sh"
