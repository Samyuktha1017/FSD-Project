#!/usr/bin/env bash
# Start backend (uvicorn) and serve frontend using Python http.server
cd backend
. .venv/bin/activate 2>/dev/null || true
if ! command -v uvicorn >/dev/null 2>&1; then
  echo "Installing backend requirements..."
  python -m venv .venv || true
  . .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
fi
# Start backend in background
uvicorn main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
echo "Backend started (pid $BACKEND_PID). Serving frontend on http://127.0.0.1:5173"
cd ../frontend
python -m http.server 5173
# When server stops, kill backend
kill $BACKEND_PID || true
