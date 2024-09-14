#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

docker-compose build --no-cache

# Build and start the Docker services
echo "Starting Docker services..."
docker-compose up --build -d

docker attach main_app