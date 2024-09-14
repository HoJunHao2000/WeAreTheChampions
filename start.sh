#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Build the Docker services
echo "Building Docker services..."
docker-compose build --no-cache

# Build and start the Docker services
echo "Starting Docker services..."
docker-compose up --build -d

# Attach to the main_app container
echo "Attaching to the main_app container..."
docker attach main_app