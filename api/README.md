# Todo App — Backend (FastAPI)

This folder will contain the FastAPI backend for Phase II of the Todo app.

Getting started (developer):

1. Create a virtual environment and install dependencies (Poetry recommended):

```bash
cd api
poetry install
poetry run uvicorn todo.main:app --reload
```

Notes:
- The real implementation will include SQLModel models, Alembic migrations, and test harness.
- This README is a scaffold placeholder created by T001.
