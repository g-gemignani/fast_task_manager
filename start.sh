#!/usr/bin/env bash
set -euo pipefail

# start.sh - start API (uvicorn) in background and run GUI in foreground
# Usage: run inside `nix-shell` created for this project (or ensure uvicorn is available)

ROOT="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$ROOT/src:$ROOT/result/lib/python$(python -c 'import sys;print(f"{sys.version_info.major}.{sys.version_info.minor}")')/site-packages:$PYTHONPATH"

echo "Starting API (uvicorn) on http://127.0.0.1:8000 ..."
uvicorn fast_task_manager.main:app --port 8000 &
API_PID=$!

trap 'echo "Shutting down..."; kill "$API_PID" 2>/dev/null || true; wait "$API_PID" 2>/dev/null || true' EXIT INT TERM

echo "Starting GUI on http://127.0.0.1:8080 ..."
python -m fast_task_manager.gui

echo "GUI exited, shutting down API (pid $API_PID)"
kill "$API_PID" 2>/dev/null || true
wait "$API_PID" 2>/dev/null || true
