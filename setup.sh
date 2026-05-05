#!/bin/bash

# Setup script for local development

echo "Setting up Multi-Agent RAG Chatbot..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys!"
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize vector stores
echo "Initializing vector stores..."
python vector_store.py

echo "✓ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Make sure you've added your API keys to .env"
echo "2. Run: python app.py"
echo "3. Open http://localhost:7860 in your browser"
