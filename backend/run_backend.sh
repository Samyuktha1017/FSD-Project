#!/usr/bin/env bash
set -e
echo "Creating venv (if missing) and installing requirements..."
python -m venv .venv || true
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Starting uvicorn on 127.0.0.1:8000 (reload)..."
uvicorn main:app --reload --host 127.0.0.1 --port 8000
