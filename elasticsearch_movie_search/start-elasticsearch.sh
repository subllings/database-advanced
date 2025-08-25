#!/bin/bash

# cd /e/_SoftEng/_BeCode/database-advanced/elasticsearch_movie_search
# chmod +x start-elasticsearch.sh
# ./start-elasticsearch.sh

# Start Elasticsearch Script
# This script starts Elasticsearch using Docker Compose

echo "Starting Elasticsearch for Movie Search Engine..."
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "ERROR: Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

# Navigate to the project directory
cd "$(dirname "$0")"

echo "Starting Elasticsearch and Kibana containers..."

# Start the services
docker-compose up -d

# Wait for Elasticsearch to be ready
echo "Waiting for Elasticsearch to be ready..."
sleep 10

# Check Elasticsearch health
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -s http://localhost:9200/_cluster/health > /dev/null 2>&1; then
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
    echo "Check logs with: docker-compose logs elasticsearch"
    exit 1
fi

# Check Elasticsearch status
echo "Elasticsearch Status:"
curl -s http://localhost:9200/_cluster/health?pretty

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
echo "To stop: ./stop-elasticsearch.sh or docker-compose down"
