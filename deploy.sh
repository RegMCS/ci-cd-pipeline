#!/bin/bash

# Deployment script for EC2 instance
# This script pulls the latest image from Docker Hub and deploys it

set -e  # Exit on any error

# Configuration
IMAGE_NAME="regsim/ci-cd-pipeline"
CONTAINER_NAME="fastapi-app"
PORT="8000"

echo "🚀 Starting deployment..."

# Login to Docker Hub
echo "🔐 Logging into Docker Hub..."
echo "$DOCKERHUB_TOKEN" | docker login docker.io -u "$DOCKERHUB_USERNAME" --password-stdin

# Pull the latest image
echo "📥 Pulling latest image: $IMAGE_NAME:latest"
docker pull "$IMAGE_NAME:latest"

# Stop existing container if running
echo "🛑 Stopping existing container..."
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

# Run the new container
echo "🏃 Starting new container..."
echo "📋 Environment variables:"
echo "  DB_HOST: $DB_HOST"
echo "  DB_PORT: $DB_PORT"
echo "  DB_NAME: $DB_NAME"
echo "  DB_USER: $DB_USER"
echo "  DB_PASSWORD: [HIDDEN]"
echo "  DB_MIN_CONN: $DB_MIN_CONN"
echo "  DB_MAX_CONN: $DB_MAX_CONN"
echo "  IMAGE_NAME: $IMAGE_NAME"
echo "  CONTAINER_NAME: $CONTAINER_NAME"
echo "  PORT: $PORT"

docker run -d \
  --name "$CONTAINER_NAME" \
  --restart unless-stopped \
  --network host \
  -p "$PORT:8000" \
  -e DB_HOST="$DB_HOST" \
  -e DB_PORT="$DB_PORT" \
  -e DB_NAME="$DB_NAME" \
  -e DB_USER="$DB_USER" \
  -e DB_PASSWORD="$DB_PASSWORD" \
  -e DB_MIN_CONN="$DB_MIN_CONN" \
  -e DB_MAX_CONN="$DB_MAX_CONN" \
  "$IMAGE_NAME:latest"

# Wait for container to start
echo "⏳ Waiting for container to start..."
sleep 10

# Health check
echo "🔍 Running health check..."
if curl -f "http://localhost:$PORT/api/v1/health" > /dev/null 2>&1; then
  echo "✅ Health check passed! Deployment successful."
else
  echo "❌ Health check failed! Check container logs:"
  docker logs "$CONTAINER_NAME"
  exit 1
fi

# Clean up old images
echo "🧹 Cleaning up old images..."
docker image prune -f

echo "🎉 Deployment completed successfully!"
