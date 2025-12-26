# Hackathon2-Todo

Monorepo scaffold for Phase II of the Todo app. Contains:

- `web/` — Next.js frontend
- `api/` — FastAPI backend
- `specs/` — specifications, plan, and tasks

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 22+
- PostgreSQL (or a compatible DB like Neon)

### Backend (API)
1. Navigate to `api/`:
   ```bash
   cd api
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your local database URL
   ```
4. Run migrations:
   ```bash
   poetry run alembic upgrade head
   ```
5. Start the server:
   ```bash
   poetry run uvicorn todo.main:app --reload
   ```

### Frontend (Web)
1. Navigate to `web/`:
   ```bash
   cd web
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```

## CI/CD
GitHub Actions are configured in `.github/workflows/ci.yml` to run linting and builds on every push.

## Phase I (Legacy)
Run the original console application:

```bash
python main.py
```

Features:

- Add task (title + optional description)
- View all tasks
- Update task (title/description)
- Delete task
- Mark complete/incomplete

Notes:

- Storage is in-memory only (no files or databases). Exiting the app loses all tasks.
- Python 3.13+ recommended.
