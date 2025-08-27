#!/bin/bash

# Navigate to project directory first: cd /e/_SoftEng/_BeCode/database-advanced/neo4j_movie_graph
# Make this file executable: chmod +x stop-neo4j.sh
# Run it with: ./scripts/stop-neo4j.sh
# chmod +x scripts/stop-neo4j.sh && ./scripts/stop-neo4j.sh

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
