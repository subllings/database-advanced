#!/bin/bash

# Navigate to project directory: cd /e/_SoftEng/_BeCode/database-advanced/elasticsearch_movie_search
# Make executable: chmod +x run-movie-search.sh
# Run with: ./run-movie-search.sh

# Run Movie Search Engine
# This script runs the complete movie search application

echo "Starting Movie Search Engine Application..."
echo "=============================================="

# Navigate to the project directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "ERROR: Virtual environment not found. Please run ./setup-env.sh first"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/Scripts/activate

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

# Check if Elasticsearch is running
echo "Checking Elasticsearch connection..."
if ! curl -s http://localhost:9200 > /dev/null 2>&1; then
    echo "ERROR: Elasticsearch is not running!"
    echo "Please start Elasticsearch first: ./start-01-elasticsearch.sh"
    exit 1
fi

echo "SUCCESS: Elasticsearch is running"

# Run the application
echo "Starting Movie Search Engine..."
echo ""

python main.py

echo ""
echo "Movie Search Engine session ended"
