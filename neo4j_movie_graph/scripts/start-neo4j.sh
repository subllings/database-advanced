#!/bin/bash

echo "Starting Neo4j Movie Graph..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "Using 'docker compose' command..."
    DOCKER_COMPOSE="docker compose"
else
    echo "Using 'docker-compose' command..."
    DOCKER_COMPOSE="docker-compose"
fi

# Start Neo4j
echo "Starting Neo4j container..."
$DOCKER_COMPOSE up -d

# Wait for Neo4j to be ready
echo "Waiting for Neo4j to be ready..."
sleep 15

# Check if Neo4j is responding
echo "Checking Neo4j connection..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -s http://localhost:7474 > /dev/null 2>&1; then
        echo "Neo4j is ready!"
        break
    else
        echo "Attempt $attempt/$max_attempts: Neo4j not ready yet..."
        sleep 2
        attempt=$((attempt + 1))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "Error: Neo4j failed to start properly"
    exit 1
fi

echo ""
echo "Neo4j Movie Graph is running!"
echo ""
echo "Neo4j Browser:"
echo "  URL: http://localhost:7474"
echo "  Username: neo4j"
echo "  Password: password123"
echo ""
echo "Neo4j Bolt Connection:"
echo "  Host: localhost"
echo "  Port: 7687"
echo "  Username: neo4j"
echo "  Password: password123"
echo ""
echo "To stop the service, run: ./scripts/stop-neo4j.sh"
