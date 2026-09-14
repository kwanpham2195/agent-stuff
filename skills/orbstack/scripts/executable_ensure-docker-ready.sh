#!/usr/bin/env bash

set -euo pipefail

TIMEOUT_SECONDS="${1:-60}"

if docker info >/dev/null 2>&1; then
  echo "Docker is ready"
  exit 0
fi

if command -v orbctl >/dev/null 2>&1; then
  echo "Docker is not ready. Checking OrbStack with orbctl..."
  if ! orbctl status >/dev/null 2>&1; then
    echo "Starting OrbStack with orbctl..."
    orbctl start
  fi
elif command -v orb >/dev/null 2>&1; then
  echo "Docker is not ready. Checking OrbStack with orb..."
  if ! orb status >/dev/null 2>&1; then
    echo "Starting OrbStack with orb..."
    orb start
  fi
else
  echo "Docker is not ready. Starting OrbStack app..."
  open -a OrbStack
fi

echo "Waiting for Docker..."
deadline=$((SECONDS + TIMEOUT_SECONDS))
while (( SECONDS < deadline )); do
  if docker info >/dev/null 2>&1; then
    echo "Docker is ready"
    exit 0
  fi
  sleep 2
done

echo "Docker did not become ready within ${TIMEOUT_SECONDS}s" >&2
exit 1
