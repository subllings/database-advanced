#!/bin/bash

# Navigate to project directory first: cd /e/_SoftEng/_BeCode/database-advanced/elasticsearch_movie_search
# Make this file executable: chmod +x start-elasticsearch.sh
# Run it with: ./start-elasticsearch.sh
# chmod +x start-elasticsearch.sh && ./start-elasticsearch.sh

# Start Elasticsearch Script
# This script starts Elasticsearch using Docker Compose

echo "Starting Elasticsearch for Movie Search Engine..."
echo "=================================================="

# Check if Docker is running (simplified check)
echo "Checking Docker status..."
# Try different ways to access docker
if command -v docker &> /dev/null; then
    DOCKER_CMD="docker"
elif command -v docker.exe &> /dev/null; then
    DOCKER_CMD="docker.exe"
elif [ -f "/c/Program Files/Docker/Docker/resources/bin/docker.exe" ]; then
    DOCKER_CMD="/c/Program Files/Docker/Docker/resources/bin/docker.exe"
else
    echo "Docker command not found, but continuing anyway since Docker Desktop is running..."
    DOCKER_CMD="docker"
fi

$DOCKER_CMD info > /dev/null 2>&1 || {
    echo "Note: Cannot verify Docker status from Git Bash, but continuing..."
    echo "Assuming Docker Desktop is running as shown in your screenshot."
}

# Check if docker-compose is available
if command -v docker-compose &> /dev/null; then
    echo "Using 'docker-compose' command..."
    DOCKER_COMPOSE="docker-compose"
elif command -v docker.exe &> /dev/null; then
    echo "Using 'docker.exe compose' command..."
    DOCKER_COMPOSE="docker.exe compose"
else
    echo "Using 'docker compose' command..."
    DOCKER_COMPOSE="docker compose"
fi

# Navigate to the project directory
cd /e/_SoftEng/_BeCode/database-advanced/elasticsearch_movie_search

echo "Starting Elasticsearch and Kibana containers..."

# Start the services
$DOCKER_COMPOSE up -d

# Wait for Elasticsearch to be ready
echo "Waiting for Elasticsearch to be ready..."
sleep 10

# Check Elasticsearch health
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    # Use Python to check instead of curl
    python -c "
import requests
try:
    r = requests.get('http://localhost:9200/_cluster/health', timeout=5)
    if r.status_code == 200:
        exit(0)
    else:
        exit(1)
except:
    exit(1)
" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "SUCCESS: Elasticsearch is ready!"
        break
    else
        echo "Attempt $attempt/$max_attempts - Waiting for Elasticsearch..."
        sleep 5
        ((attempt++))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "ERROR: Elasticsearch failed to start after $max_attempts attempts"
    echo "Check logs with: $DOCKER_COMPOSE logs elasticsearch"
    exit 1
fi

# Check Elasticsearch status using Python
echo "Elasticsearch Status:"
python -c "
import requests
try:
    r = requests.get('http://localhost:9200/_cluster/health?pretty', timeout=5)
    print(r.text)
except Exception as e:
    print(f'Error getting status: {e}')
"

echo ""
echo "SUCCESS: Elasticsearch is now running!"
echo "=================================================="
echo "Elasticsearch: http://localhost:9200"
echo "Kibana (optional): http://localhost:5601"
echo ""
echo "Next steps:"
echo "   1. Run: python main.py"
echo "   2. Or test connection: python test_basic.py --connection-only"
echo ""
echo "To stop: ./stop-elasticsearch.sh or $DOCKER_COMPOSE down"
