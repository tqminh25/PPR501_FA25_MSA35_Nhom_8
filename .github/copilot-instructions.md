## Quick context

This repository is a small Student Management project with a FastAPI backend, a tkinter desktop UI that talks to the API, and a few scripts that call the same API.

High-level components
- backend/app — FastAPI service (SQLAlchemy + Pydantic). Entry point: `backend.app.main:app` (variable `app`).
- desktop/main_gui.py — tkinter desktop client that calls API at `http://127.0.0.1:8000`.
- scripts/crawl_students.py — simple crawler that GETs `/students` and writes `data/students_raw.*`.
- students.db — SQLite database file at repository root (used by SQLAlchemy URL `sqlite:///./students.db`).

## How to run locally (developer tasks)
- Start the backend API (recommended):

  uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000

  Notes: `routers/students.py` calls `Base.metadata.create_all(bind=engine)` on import so the SQLite file (`students.db`) will be created automatically when the API is started.

- Run the desktop GUI (requires the API to be running):

  python desktop/main_gui.py

- Crawl data script (expects API running):

  python scripts/crawl_students.py

If you run Python from a directory other than the repository root, the relative SQLite URL (`./students.db`) will resolve relative to the current working directory. Prefer launching commands from the project root.

## Key design & patterns to follow (concrete, discoverable)
- API structure: routers use dependency `get_db()` which yields a `SessionLocal()` (see `backend/app/routers/students.py` and `backend/app/db.py`). Use that pattern for DB access.
- Pydantic shapes: incoming payloads are `schemas.StudentIn` and responses `schemas.StudentOut` (see `backend/app/schemas.py`). New code that accepts student payloads should use these models.
- Uniqueness handling: `crud.create_student` and `crud.update_student` raise ValueError("student_code exists") or ValueError("email exists"). The desktop client detects the string "exists" in error detail to classify duplicates — preserve these messages or change both client + API together.
- Status codes used by convention:
  - POST /students -> 201 on success
  - GET /students/{id} -> 200 or 404
  - DELETE /students/{id} -> 204 on success
  - Validation/duplicate -> 400 with detail text (often contains "exists")

## Files to inspect when changing behavior
- Data model: `backend/app/models.py` (SQLAlchemy model `Student`).
- CRUD logic + uniqueness rules: `backend/app/crud.py`.
- API surface & DB init: `backend/app/routers/students.py`.
- DB configuration: `backend/app/db.py` (SQLAlchemy engine uses `sqlite:///./students.db`).
- Desktop CSV header canonicalization: `desktop/main_gui.py` defines `FIELDS` and `CSV_HEADERS`. If you change field names in the model, update this file and `scripts/crawl_students.py` accordingly.

## Common integration gotchas & debugging tips
- Duplicate detection: the frontend/importer checks for the substring "exists" in error details. If you change duplication error messages in `crud.py`, update the import logic in `desktop/main_gui.py`.
- DB path: `DATABASE_URL` is `sqlite:///./students.db`. If tests or CI run from a different cwd, create a temporary DB or set `DATABASE_URL` accordingly.
- Query behavior: `crud.list_students` uses `ilike` for case-insensitive search across student_code, first_name, last_name, email. Keep this in mind when implementing search enhancements.
- Direct model access: some places query `crud.models.Student` or import `models` indirectly. When refactoring models, update all usages.
- Quick DB inspection: open `students.db` with `sqlite3 students.db` or DB Browser to inspect records.

## Example snippets (copy-paste)
- Start API (dev):

  uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000

- Create a student via curl (desktop importer expects the same shape as `schemas.StudentIn`):

  curl -X POST "http://127.0.0.1:8000/students" -H "Content-Type: application/json" -d '{"student_code":"S001","first_name":"A","last_name":"Nguyen","email":"a@x.com"}'

- Get students (large export):

  curl "http://127.0.0.1:8000/students?limit=10000"

## Small policy notes for AI agents
- Preserve the concrete error strings used by the desktop UI when touching uniqueness checks (see `crud.create_student` and `desktop/main_gui.py`).
- When editing the DB URL or model fields, update `desktop/main_gui.py` `FIELDS` and `CSV_HEADERS` in lockstep; they are canonical for CSV import/export.
- Changes that affect API responses (status codes or JSON shape) require updating the desktop GUI and `scripts/crawl_students.py` because they assume the current contract.

## Where to start for typical tasks
- Add a new student field: update `models.py` -> `schemas.py` (Pydantic) -> `desktop/main_gui.py` FIELDS/CSV_HEADERS -> add migrations or rely on `create_all` (note: SQLite and `create_all` won't migrate existing columns).
- Fix a bug in duplicate handling: look in `crud.py` for ValueError messages, and `desktop/main_gui.py` for the duplicate handling branch.

If anything here is unclear or you need more detailed examples (tests, CI commands, or a requirements list), tell me which area to expand and I'll iterate.
