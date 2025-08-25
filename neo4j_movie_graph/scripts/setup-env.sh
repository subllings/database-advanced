#!/bin/bash

echo "Setting up Neo4j Movie Graph environment..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Using Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/Scripts/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt

echo "Environment setup complete!"
echo ""
echo "To activate the environment manually, run:"
echo "source .venv/Scripts/activate"
echo ""
echo "Next steps:"
echo "1. Run './scripts/start-neo4j.sh' to start Neo4j"
echo "2. Run './scripts/run-graph.sh' to start the application"
