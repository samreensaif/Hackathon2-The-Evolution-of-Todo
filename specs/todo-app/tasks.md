---
title: Phase II Implementation Tasks (speckit.tasks)
feature: todo-app
version: 2.0.0
created: 2025-12-25
approved: true
approved_by: team
approved_date: 2025-12-25
locked: true
lock_note: Tasks approved and locked for implementation; edits require a PR and explicit approval.
---

# Phase II — Atomic Implementation Tasks

Status: Approved and locked for implementation on 2025-12-25.

This file breaks the Phase II plan into small, atomic, sequential tasks suitable for spec‑driven implementation and assignment. Each task includes a short description, acceptance criteria, and dependencies.

## Sprint 1 — Foundation

- T001 — Scaffold repositories
  - Description: Create `web/` (Next.js TypeScript) and `api/` (FastAPI) repositories, initial README, and `.gitignore` entries.
  - Acceptance: `web/` and `api/` folders exist with package manifests (`package.json`/`pyproject.toml`) and README placeholders.
  - Depends on: none

- T002 — CI/CD baseline
  - Description: Add GitHub Actions skeletons for lint/test/build for frontend and backend; CI should run unit tests and linters.
  - Acceptance: PR pipeline runs and reports lint/test status in CI (no production deploy yet).
  - Depends on: T001

- T003 — DB & migrations setup
  - Description: Add SQLModel models for `users` and `tasks` and configure Alembic with initial migration.
  - Acceptance: Alembic migration file created and `alembic upgrade head` applies schema locally.
  - Depends on: T001

- T004 — Auth integration spike (BetterAuth)
  - Description: Prototype verifying BetterAuth tokens and/or exchange flow to assess token ownership model.
  - Acceptance: Spike notes document whether backend will trust BetterAuth tokens or issue its own JWTs, with pros/cons.
  - Depends on: T001

- T005 — Dev environment & secrets
  - Description: Add `.env.example`, local dev DB config, and instructions for Neon connection strings via secret manager.
  - Acceptance: Developers can run backend locally pointing to a dev DB using provided env samples.
  - Depends on: T003

## Sprint 2 — Core Backend & Auth

- T006 — Implement auth middleware
  - Description: FastAPI middleware that validates JWTs, sets `current_user` in request context.
  - Acceptance: Protected endpoint rejects requests without valid JWT (401) and populates `current_user` on success.
  - Depends on: T003, T004

- T007 — User account endpoints
  - Description: Implement registration/login endpoints (or integration endpoints if BetterAuth handles registration).
  - Acceptance: Registration creates a `users` row; login returns access token payload per spec.
  - Depends on: T003, T004

- T008 — Task CRUD endpoints (basic)
  - Description: Implement `GET /api/v1/tasks`, `POST /api/v1/tasks`, `GET /api/v1/tasks/{id}`, `PATCH`, `DELETE` with ownership checks.
  - Acceptance: Endpoints follow API contract; unauthorized access returns 401; accessing other user's task returns 404/403.
  - Depends on: T006, T007

- T009 — Tests for backend
  - Description: Add unit tests for services and integration tests against a test Postgres instance.
  - Acceptance: CI runs backend tests; sample integration test covers creating a user and CRUDing a task.
  - Depends on: T006, T008

## Sprint 3 — Frontend Implementation

- T010 — Next.js auth pages
  - Description: Implement login and registration pages and client token handling per chosen model (httpOnly cookie or in-memory access token).
  - Acceptance: User can log in and obtain token; frontend stores token securely and includes it on API requests.
  - Depends on: T007, decision from T004

- T011 — Task list UI
  - Description: Implement task listing page with pagination, filters (`completed`), and search box; show creation and update timestamps.
  - Acceptance: Page displays items from `GET /api/v1/tasks` and correctly reflects filtering/pagination.
  - Depends on: T008, T010

- T012 — Task create/edit components
  - Description: Implement create and edit UI (modal or page) with client validation for title non‑empty.
  - Acceptance: Creating/updating tasks calls API and updates list (optimistic update optional but reconciles with server state).
  - Depends on: T008, T011

- T013 — E2E tests for key flows
  - Description: Write Playwright/Cypress tests for register→login→create→list→update→delete flows.
  - Acceptance: E2E tests run in CI and pass against staging environment.
  - Depends on: T010, T011, T012

## Sprint 4 — Harden, Ops, and Release

- T014 — Pagination, filtering, search enhancements
  - Description: Backend and frontend improvements to support efficient pagination and search; add DB indexes.
  - Acceptance: Large task lists paginate correctly and maintain p95 targets under light load.
  - Depends on: T008, T011

- T015 — Logging & monitoring
  - Description: Add structured logs, error aggregation configuration, and basic metrics (request counts, error rates, latency).
  - Acceptance: Alerting thresholds documented; logs captured by chosen provider in staging.
  - Depends on: T008, T011

- T016 — Backups & migrations runbook
  - Description: Document Neon backup schedule, restore steps, and migration execution procedure for Alembic during deploy.
  - Acceptance: Ops runbook created and verified in staging (dry run of backup/restore documented).
  - Depends on: T003

- T017 — Final acceptance & release
  - Description: Run acceptance checklist: register/login/create/list/update/delete, security checks, CI green, deploy to production.
  - Acceptance: All acceptance criteria in `spec.md` pass; release notes drafted.
  - Depends on: T013, T014, T015, T016

## Cross‑cutting Tasks

- TX01 — OpenAPI / API docs
  - Description: Produce an OpenAPI (Swagger) spec from implemented endpoints and keep it in `specs/`.
  - Acceptance: OpenAPI file exists and matches live API in staging.
  - Depends on: T008

- TX02 — Security review
  - Description: Conduct a security checklist (JWT handling, TLS, CORS, input validation, rate limits).
  - Acceptance: Security issues logged and mitigations planned.
  - Depends on: T006, T007, T008

- TX03 — Migration tool for Phase I data
  - Description: Provide a one‑off import tool and docs to migrate in‑memory tasks to DB, mapping to user accounts.
  - Acceptance: Migration can import example Phase I dataset into staging DB and associate tasks with a chosen user.
  - Depends on: T003

---

Each task should be split further into implementation subtasks by the assignee as needed (tests, docs, CI changes). Tasks are intentionally small and ordered so that earlier tasks unlock later work.
