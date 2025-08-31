# Magnus CRUD Demo (FastAPI + SQLite + React CDN)

A minimal full‑stack sample that covers CRUD and common "More" menu options (bulk delete, import CSV, export CSV, search, filter, sort, pagination).

## Run backend

```bash
cd backend
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs at `http://127.0.0.1:8000/docs`

## Run frontend (static)

Just open `frontend/index.html` in a browser, or serve the folder with any static server.

On Windows you can run:

```bash
python -m http.server 5173 --directory frontend
```

Then open http://localhost:5173

## Sample CSV

Use `sample-employees.csv` to import.
