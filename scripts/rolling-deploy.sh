#!/bin/bash
set -e

SERVICE=$1       # e.g. "api"
NEW_IMAGE=$2     # e.g. "myrepo/api:abc1234"

TEMP_NAME="${SERVICE}_new"
TIMEOUT=60
ELAPSED=0

echo "Starting new container: $TEMP_NAME"
docker run -d --name "$TEMP_NAME" "$NEW_IMAGE"

echo "Waiting for health check (up to ${TIMEOUT}s)..."
while [ $ELAPSED -lt $TIMEOUT ]; do
  STATUS=$(docker inspect --format='{{.State.Health.Status}}' "$TEMP_NAME" 2>/dev/null || echo "none")
  if [ "$STATUS" = "healthy" ]; then
    echo "New container is healthy. Stopping old container..."
    docker stop "$SERVICE" 2>/dev/null || true
    docker rm "$SERVICE" 2>/dev/null || true
    docker rename "$TEMP_NAME" "$SERVICE"
    echo "Rolling deploy successful."
    exit 0
  fi
  sleep 2
  ELAPSED=$((ELAPSED + 2))
done

echo "Health check failed after ${TIMEOUT}s. Aborting. Old container left running."
docker stop "$TEMP_NAME" 2>/dev/null || true
docker rm "$TEMP_NAME" 2>/dev/null || true
exit 1
