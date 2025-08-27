#!/bin/bash

# Navigate to project directory first: cd /e/_SoftEng/_BeCode/database-advanced/elasticsearch_movie_search
# Make this file executable: chmod +x stop-elasticsearch.sh
# Run it with: ./stop-elasticsearch.sh
# chmod +x stop-elasticsearch.sh && ./stop-elasticsearch.sh

# 🛑 Stop Elasticsearch Script
# This script stops the Elasticsearch containers

echo "🛑 Stopping Elasticsearch for Movie Search Engine..."
echo "=================================================="

# Navigate to the project directory
cd "$(dirname "$0")"

# Stop the services
echo "🐳 Stopping Docker containers..."
docker-compose down

if [ $? -eq 0 ]; then
    echo "✅ Elasticsearch and Kibana stopped successfully"
else
    echo "❌ Failed to stop some containers"
fi

# Optional: Remove volumes (uncomment if you want to clear all data)
# echo "🗑️ Removing volumes and data..."
# docker-compose down -v

echo ""
echo "🔍 Container status:"
docker ps -a --filter "name=movie-search"

echo ""
echo "✨ Cleanup complete!"
