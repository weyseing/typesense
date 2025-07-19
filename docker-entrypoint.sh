#!/bin/sh

# start typesense
echo "[ENTRYPOINT] Starting Typesense server..."
/opt/typesense-server --data-dir /data --api-key=${TYPESENSE_API_KEY} --enable-cors --listen-address 0.0.0.0 &

# health check
echo "[ENTRYPOINT] Waiting for Typesense /health endpoint..."
until curl -sf http://localhost:8108/health | grep -q '"ok":true'; do
  HEALTH_RESULT=$(curl -sf http://localhost:8108/health || echo 'Failed to connect')
  echo "[ENTRYPOINT] Health check response: $HEALTH_RESULT"
  sleep 2
done
HEALTH_RESULT=$(curl -sf http://localhost:8108/health)
echo "[ENTRYPOINT] Typesense /health endpoint is healthy! Response: $HEALTH_RESULT"

# debug check
echo "[ENTRYPOINT] Waiting for Typesense /debug endpoint..."
until curl -sf -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" http://localhost:8108/debug | grep -q '"version":'; do
  DEBUG_RESULT=$(curl -sf -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" http://localhost:8108/debug || echo 'Failed to connect')
  echo "[ENTRYPOINT] Debug check response: $DEBUG_RESULT"
  sleep 2
done
DEBUG_RESULT=$(curl -sf -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" http://localhost:8108/debug)
echo "[ENTRYPOINT] Typesense /debug endpoint is accessible! Response: $DEBUG_RESULT"

# keep the container running
wait