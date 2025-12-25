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

Alembic migrations:

This project includes an `alembic/` scaffold and an initial migration
(`alembic/versions/0001_initial.py`). To run migrations locally set the
`DATABASE_URL` environment variable and run:

```bash
cd api
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/todo_dev
alembic -c alembic.ini upgrade head
```

Note: On Windows use the platform-appropriate way of setting env vars. The
initial migration bootstraps tables from `sqlmodel` metadata (convenient for
Phase II development); production teams should review migrations before applying.
