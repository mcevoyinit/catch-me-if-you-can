#!/bin/bash

echo "Starting Catch Me If You Can Protocol Demo..."
echo "============================================"

# Check Python installation
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is required but not installed."
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "Running demo..."
python main.py demo

echo "Demo complete!"