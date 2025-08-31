\
    @echo off
    python -m venv .venv
    call .venv\Scripts\activate
    pip install --upgrade pip
    pip install -r requirements.txt
    uvicorn main:app --reload --host 127.0.0.1 --port 8000
