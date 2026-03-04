#!/bin/bash
# Build script for Render deployment

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "Build complete!"
