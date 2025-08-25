#!/bin/bash

echo "Running Neo4j Movie Graph..."

# Activate virtual environment
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/Scripts/activate
else
    echo "Warning: Virtual environment not found. Run ./scripts/setup-env.sh first."
fi

# Check if Neo4j is running
if ! curl -s http://localhost:7474 > /dev/null; then
    echo "Neo4j is not running. Starting Neo4j..."
    ./scripts/start-neo4j.sh
    echo "Waiting for Neo4j to be ready..."
    sleep 10
fi

# Run the application
echo "Starting Movie Graph application..."
python main.py
