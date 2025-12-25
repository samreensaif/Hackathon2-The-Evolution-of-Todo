<!--
Sync Impact Report:
Version change: N/A (old) -> 1.0.0 (new)
Modified principles: None
Added sections: None
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ updated (no specific updates needed beyond generic placeholder alignment)
  - .specify/templates/tasks-template.md: ✅ updated (no specific updates needed beyond generic placeholder alignment)
  - .specify/templates/commands/*.md: ✅ updated (no specific updates needed beyond generic placeholder alignment)
Follow-up TODOs: None
-->
# Feature Specification: Todo App — Phase II (Full‑stack Web Application)

**Feature Branch**: `phase/feature/webui-multitenant` (proposed)
**Created**: 2025-12-25
**Status**: Draft — Phase II (WHAT only)
**Scope**: Convert the Phase I console app into a full‑stack, multi‑user web application with persistent storage, a REST API, and JWT authentication. This document specifies WHAT the system must do (requirements, user stories, API contracts, acceptance criteria). It intentionally avoids implementation details (HOW).

## Goals

- Replace the single‑user console UI with a browser‑based UI (SPA or server‑rendered) and a RESTful backend.
- Support multiple users with isolated data (each user sees only their tasks).
- Persist tasks to a durable database for long‑term storage.
- Expose a well‑documented REST API to enable web UI and third‑party clients.
- Protect user data with authentication and authorization using JWTs.

## Non‑Goals

- Real‑time collaboration (websockets) — out of scope for Phase II.
- Social features (sharing tasks between users) — out of scope unless explicitly requested later.

## Key User Stories (WHAT)

### US-1: User registration and authentication (P0)
As an unauthenticated person, I can register an account and obtain credentials; as an authenticated user, I can log in and receive a JWT for subsequent requests.

Acceptance criteria:
- Registration endpoint exists and validates unique email/username.
- Login endpoint returns a signed JWT and refresh token (if refresh tokens are used; refresh token usage is optional for Phase II but allowed).

### US-2: Multi‑user task management (P0)
As an authenticated user, I can create, view, update, and delete my tasks; I must not be able to access other users' tasks.

Acceptance criteria:
- All task endpoints are scoped to the authenticated user.
- Users see only their tasks in listings and queries.

### US-3: Persistent storage (P0)
Tasks and user accounts are persisted in a database so data survives restarts.

Acceptance criteria:
- Data persists across server restarts in the chosen DB.
- Migration plan exists for moving in‑memory data (if any) to the DB.

### US-4: REST API for all core operations (P0)
A documented REST API exposes endpoints for auth, task CRUD, and task queries.

Acceptance criteria:
- API specification (endpoints, request/response schemas, error codes) is included in this spec.

### US-5: Secure API (P0)
All endpoints that operate on user data require a valid JWT; token expiry and verification behavior are specified.

Acceptance criteria:
- Unauthorized requests return 401 (or 403 where applicable).

## API Contract (WHAT)

Notes: JSON request/response bodies. Use standard HTTP status codes. All endpoints below that operate on user data require an `Authorization: Bearer <JWT>` header unless noted otherwise.

Auth
- POST /api/v1/auth/register
  - Request: { "email": string, "password": string, "name"?: string }
  - Response: 201 Created { "id": string, "email": string }
  - Errors: 400 (validation), 409 (email exists)

- POST /api/v1/auth/login
  - Request: { "email": string, "password": string }
  - Response: 200 OK { "accessToken": string, "expiresIn": int, "refreshToken"?: string }
  - Errors: 400, 401

- POST /api/v1/auth/refresh (optional)
  - Request: { "refreshToken": string }
  - Response: 200 OK { "accessToken": string, "expiresIn": int }

Tasks
- GET /api/v1/tasks
  - Query params: `?completed=true|false` (optional), `?q=search` (optional), pagination params (`page`, `limit`) optional
  - Response: 200 OK { "items": [Task], "total": int }

- POST /api/v1/tasks
  - Request: { "title": string, "description"?: string }
  - Response: 201 Created { Task }
  - Errors: 400 (validation)

- GET /api/v1/tasks/{taskId}
  - Response: 200 OK { Task } or 404

- PATCH /api/v1/tasks/{taskId}
  - Request: partial Task fields, e.g. { "title"?: string, "description"?: string, "completed"?: boolean }
  - Response: 200 OK { Task } or 404 or 403

- DELETE /api/v1/tasks/{taskId}
  - Response: 204 No Content or 404

Task Model (response shape)
 - id: string (UUID or DB id)
 - userId: string (owner reference)
 - title: string
 - description: string | null
 - completed: boolean
 - createdAt: ISO8601 timestamp
 - updatedAt: ISO8601 timestamp

Error model
 - { "code": string, "message": string, "details"?: object }

Authentication & Authorization (WHAT)

 - Use JSON Web Tokens (JWT) for stateless authentication for API calls.
 - JWTs MUST include a `sub` claim referencing the user id and an `exp` claim for token expiry.
 - All protected endpoints must verify the token signature and expiry.
 - Token revocation strategy: For Phase II, token revocation may rely on short expiry times and optional refresh tokens; a server‑side blacklist is out of scope unless required later.

Persistence (WHAT)

 - Primary persistent storage: relational or document database (e.g., PostgreSQL, SQLite for dev, or a managed DB). Choice is a non‑functional/implementation decision (left to Phase II HOW decisions), but the spec requires ACID durability for tasks and users.
 - Schema (logical): `users` table/collection (id, email, password_hash, name, created_at, updated_at), `tasks` table/collection (id, user_id, title, description, completed, created_at, updated_at).

Data Migration

 - If Phase I in‑memory data must be preserved, provide a one‑time migration script to import in‑memory tasks into the DB mapping to a default user or prompting a mapping workflow. Migration HOW is deferred, but the requirement is: migration path exists and is documented.

Security & Privacy Requirements (WHAT)

 - Passwords MUST be stored using a secure hashing algorithm (e.g., bcrypt, argon2) — HOW left to implementation.
 - All sensitive tokens must be transmitted over TLS in production (enforce HTTPS in deployment).
 - The API MUST not expose other users' data; enforce owner checks on every resource access.
 - Rate limiting and brute‑force protections are recommended for auth endpoints (outlines allowed; implementation deferred).

Non‑Functional Requirements (WHAT)

 - NFR-Perf-001: The API should respond to common requests (single task CRUD) within 300ms p95 under light load (informational target; exact performance tuning is an implementation decision).
 - NFR‑Reliability‑001: Data persistence must survive server restarts; DB backups and restoration strategy must be defined in operations documentation (Phase II deliverable).
 - NFR‑Scalability‑001: System should be designed to allow horizontal scaling of stateless API servers; DB scaling strategy is out of scope for Phase II.

Observability & Ops (WHAT)

 - Basic logs for auth and task operations (INFO for success, WARN/ERROR for failures) must exist.
 - Errors should be instrumented for later aggregation (Sentry/Log service integration is an ops decision).

Acceptance Criteria (checks)

 - [ ] End‑to‑end user flow: register → login → create task → list tasks → update task → delete task (using the REST API and web UI) passes.
 - [ ] API returns proper status codes and JSON error payloads on invalid requests.
 - [ ] Authenticated user cannot access another user's tasks (tests cover 403/404 cases).
 - [ ] Tasks persist across service restarts in the chosen DB.

Deliverables (WHAT)

 - Updated `specs/todo-app/spec.md` (this file) describing Phase II requirements.
 - API documentation (OpenAPI/Swagger or markdown) describing endpoints and schemas (deliverable for Phase II implementation).
 - Migration plan for Phase I data (if required).
 - Acceptance test cases (manual or automated) covering listed acceptance criteria.

Risks & Open Questions

 - Choice of DB and migration approach may impact implementation complexity and schedule.
 - Refresh token strategy and token revocation requirements need product decision: short‑lived tokens only vs. refresh tokens with revocation store.

Version: 2.0.0 | Ratified: 2025-12-25 | Last Amended: 2025-12-25
