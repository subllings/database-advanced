#!/bin/bash

echo "Starting MongoDB Library Catalog..."

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

# Start MongoDB and Mongo Express
echo "Starting MongoDB and Mongo Express containers..."
$DOCKER_COMPOSE up -d

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to be ready..."
sleep 10

# Check if MongoDB is responding
echo "Checking MongoDB connection..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if docker exec mongodb_library mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
        echo "MongoDB is ready!"
        break
    else
        echo "Attempt $attempt/$max_attempts: MongoDB not ready yet..."
        sleep 2
        attempt=$((attempt + 1))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "Error: MongoDB failed to start properly"
    exit 1
fi

echo ""
echo "MongoDB Library Catalog is running!"
echo ""
echo "MongoDB Connection:"
echo "  Host: localhost"
echo "  Port: 27017"
echo "  Username: admin"
echo "  Password: password123"
echo ""
echo "Mongo Express (Web Interface):"
echo "  URL: http://localhost:8081"
echo "  Username: admin"
echo "  Password: password123"
echo ""
echo "To stop the services, run: ./scripts/stop-mongodb.sh"
