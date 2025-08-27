#!/bin/bash

# Navigate to project directory first: cd /e/_SoftEng/_BeCode/database-advanced/elasticsearch_movie_search
# Make this file executable: chmod +x run-movie-search.sh
# Run it with: ./run-movie-search.sh
# chmod +x run-movie-search.sh && ./run-movie-search.sh

# Run Movie Search Engine
# This script runs the complete movie search application

echo "Starting Movie Search Engine Application..."
echo "=============================================="

# Navigate to the project directory (fixed for Git Bash)
cd /e/_SoftEng/_BeCode/database-advanced/elasticsearch_movie_search

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

# Check if Elasticsearch is running using Python instead of curl
echo "Checking Elasticsearch connection..."
python -c "
import requests
try:
    r = requests.get('http://localhost:9200', timeout=5)
    if r.status_code == 200:
        exit(0)
    else:
        exit(1)
except:
    exit(1)
" > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "ERROR: Elasticsearch is not running!"
    echo "Please start Elasticsearch first: ./start-elasticsearch.sh"
    exit 1
fi

echo "SUCCESS: Elasticsearch is running"

# Run the application
echo "Starting Movie Search Engine..."
echo ""

python main.py

echo ""
echo "Movie Search Engine session ended"
