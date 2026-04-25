#!/bin/bash
set -e

TIMEOUT=60
FRONTEND_URL="http://localhost:3000"

echo "Waiting for frontend to be ready..."
ELAPSED=0
until curl -sf "$FRONTEND_URL/health" > /dev/null; do
  sleep 2
  ELAPSED=$((ELAPSED + 2))
  if [ $ELAPSED -ge $TIMEOUT ]; then
    echo "Frontend did not become ready in ${TIMEOUT}s"
    exit 1
  fi
done

echo "Submitting a job..."
RESPONSE=$(curl -sf -X POST "$FRONTEND_URL/submit")
echo "Response: $RESPONSE"
JOB_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "Job ID: $JOB_ID"

echo "Polling for completion..."
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT ]; do
  STATUS=$(curl -sf "$FRONTEND_URL/status/$JOB_ID" | \
    python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "Status: $STATUS"
  if [ "$STATUS" = "completed" ]; then
    echo "Job completed successfully."
    exit 0
  fi
  sleep 3
  ELAPSED=$((ELAPSED + 3))
done

echo "Job did not complete within ${TIMEOUT}s"
exit 1
