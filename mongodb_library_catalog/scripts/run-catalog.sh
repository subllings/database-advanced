#!/bin/bash

echo "Running MongoDB Library Catalog..."

# Activate virtual environment
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/Scripts/activate
else
    echo "Warning: Virtual environment not found. Run ./scripts/setup-env.sh first."
fi

# Check if MongoDB is running
if ! docker ps | grep mongodb_library > /dev/null; then
    echo "MongoDB is not running. Starting MongoDB..."
    ./scripts/start-mongodb.sh
    echo "Waiting for MongoDB to be ready..."
    sleep 5
fi

# Run the application
echo "Starting Library Catalog application..."
python main.py
