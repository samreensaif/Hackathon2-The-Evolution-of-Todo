```markdown
# Plan: Phase II — Web Application Architecture & Roadmap

**Source:** [specs/todo-app/spec.md](specs/todo-app/spec.md)

**Goal:** Define the architecture and implementation plan for Phase II: front end using Next.js, backend using FastAPI, persistent DB on Neon (Postgres), data modelling and access via SQLModel, and authentication using BetterAuth with JWTs. This file focuses on architecture, responsibilities, sequencing, and acceptance checks (WHAT and high-level HOW decisions to guide implementation teams). No production code is included here.

## High‑level Architecture

- Frontend: Next.js (React, TypeScript) single‑page application (SPA) with server‑side rendering where appropriate for SEO / initial load. Client communicates with backend via REST API.
- Backend: FastAPI (Python) exposing versioned REST endpoints under `/api/v1/*`. FastAPI handles JSON I/O, request validation (Pydantic/SQLModel), and ASGI hosting.
- Database: Neon (Postgres-compatible serverless) as primary persistent store. Data access via SQLModel for typed models and migrations managed by Alembic (or equivalent).
- Authentication: BetterAuth (identity provider) integrated for user registration/management; backend verifies and issues JWTs for API access. JWTs include `sub`, `exp`, and `iat` claims.
- Deployment: Cloud hosting for frontend (e.g., Vercel) and backend (serverless or containerized on a managed service). Neon provides DB hosting; secrets stored in platform secret manager.

## Component Responsibilities

- Frontend (Next.js)
  - Pages/Routes: Login/Register, Task List (with filters/search), Task Create/Edit, Account/Profile, Settings.
  - Auth: store short‑lived access token (in memory) and refresh token if used (httpOnly cookie). Send `Authorization: Bearer <JWT>` on API calls.
  - UX: optimistic UI for create/update/delete with server reconciliation; client‑side validation for title non‑emptiness.
  - Tests: unit tests for components, E2E tests (Playwright or Cypress) for key flows.

- Backend (FastAPI)
  - API: implements REST contract in `spec.md` (auth endpoints, task CRUD). Uses SQLModel declarative models mapping to Postgres tables.
  - Auth Integration: registration/login endpoints optional if BetterAuth handles registration; backend must accept and verify BetterAuth tokens or exchange credentials to obtain JWTs. Backend issues its own signed JWTs for client usage if required, or relies on BetterAuth issued JWTs (TO DECIDE — see open questions).
  - Business Logic: `services` layer implements validations and ownership checks; `repositories` layer handles DB interactions via SQLModel sessions.
  - Migrations: Alembic configured to manage schema evolution.
  - Tests: unit tests for services, integration tests for DB (use test DB, fixtures), and contract tests for API.

- Database (Neon + SQLModel)
  - Logical schema: `users` (id UUID, email unique, password_hash if local auth, name, created_at, updated_at), `tasks` (id UUID, user_id FK, title, description, completed boolean, created_at, updated_at).
  - Indexes: index on (`user_id`, `created_at`) and `email` unique constraint.
  - Migration strategy: Alembic migration scripts; CI runs migrations or ensures migrations are applied at deploy.

- Auth (BetterAuth + JWT)
  - User lifecycle: registration → email verification (optional) → login → token issuance.
  - JWT characteristics: short lived access tokens (e.g., 15m), optional refresh tokens (rotating), `sub` claim set to user id, `roles` claim optional.
  - Revocation: Phase II relies primarily on short TTLs and optional refresh token rotation; server‑side blacklist is optional for future phases.

## Data Flow

1. User authenticates via BetterAuth or backend auth endpoint; receives JWT (and refresh token if used).
2. Frontend stores tokens securely (httpOnly cookie for refresh token; access token in memory) and sends `Authorization` header on API requests.
3. Backend middleware validates JWT signature, expiry, and extracts `sub` as `user_id` for request context.
4. Backend handlers use `user_id` to scope DB queries (tasks filtered by owner).

## Security Considerations

- Enforce TLS (HTTPS) for all client ↔ server and server ↔ BetterAuth/Neon communications.
- Store secrets in secret manager; do not commit keys.
- Protect auth endpoints with rate limiting and login brute‑force protections.
- Ensure proper owner checks on task endpoints (return 404 for non‑owned resources to avoid information leaks).

## Operational Concerns

- Observability: structured logging, distributed tracing (optional), and error aggregation (Sentry). Instrument auth failures, DB errors, and critical business errors.
- Backups: configure Neon automated backups and document restore procedure.
- CI/CD: GitHub Actions pipeline to run linting, unit tests, build frontend, run backend tests, and deploy artifacts (frontend to Vercel, backend to target platform). Apply DB migrations during deployment with safety checks.

## Implementation Plan & Milestones

Phase II is divided into 4 sprints (2–3 week cadence recommended):

- Sprint 1 — Foundation (week 1)
  - Task 1.1: Repo scaffolding: `web/` (Next.js), `api/` (FastAPI), infra manifests (deployment, env examples).
  - Task 1.2: DB & migrations: define SQLModel models and initial Alembic migration for `users` and `tasks` tables.
  - Task 1.3: Auth integration spike: prototype BetterAuth token verification flow.

- Sprint 2 — Core API & Auth (week 2)
  - Task 2.1: Implement FastAPI endpoints for task CRUD with ownership checks.
  - Task 2.2: Implement auth middleware to validate JWT and populate `current_user` in request context.
  - Task 2.3: Add unit and integration tests for services and API endpoints.

- Sprint 3 — Frontend & UX (week 3)
  - Task 3.1: Implement Next.js pages: login/register, task list, create/edit modals.
  - Task 3.2: Wire auth flows: login UI → receive tokens → call API.
  - Task 3.3: E2E tests for critical flows (register/login/create/list/update/delete).

- Sprint 4 — Harden & Release (week 4)
  - Task 4.1: Add pagination, filtering, and search to task list API and UI.
  - Task 4.2: Add logging, monitoring, and automated DB backups config.
  - Task 4.3: Run acceptance tests, finalize docs and migration plan, and cut release.

## Acceptance Criteria (Phase II)

- [ ] Frontend communicates with API over HTTPS and handles token lifecycle without exposing secrets.
- [ ] Authenticated users can perform all task CRUD operations and cannot access other users' tasks.
- [ ] Database persists tasks and users across restarts; migrations applied cleanly in staging.
- [ ] CI runs tests and linters; deploys to staging; rolling deploys to production are documented.

## Testing Strategy

- Unit tests: services and utilities.
- Integration tests: DB-backed tests using a test Postgres instance (or Dockerized Neon emulation) and test fixtures.
- Contract tests: ensure API responses match OpenAPI schemas.
- E2E tests: user flows in the browser (login, create/update/delete tasks).

## Risks & Open Questions

- BetterAuth vs local auth: Decide whether the backend issues its own JWTs or fully trusts BetterAuth tokens. Tradeoffs: centralized identity (outsourced) vs control over token lifecycle.
- Neon limits and cold starts: serverless DB may introduce latency; plan for connection pooling and retry/backoff logic.
- Refresh token strategy: rotating refresh tokens add security but require server‑side state. Product decision required.

## Next Tactical Steps

1. Agree on auth token ownership model (BetterAuth tokens vs backend‑issued JWTs).
2. Create OpenAPI draft for API endpoints (based on `spec.md`).
3. Scaffold repos and CI pipeline; create initial Alembic migration.

---

This plan complements the Phase II specification in [specs/todo-app/spec.md](specs/todo-app/spec.md). Replace Phase I console plan with this file for Phase II work.
``` 
```
