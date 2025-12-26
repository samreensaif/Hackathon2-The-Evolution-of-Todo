---
id: 0012
title: Implement Task CRUD Endpoints (T005)
stage: tasks
date_iso: 2025-12-25
surface: agent
model: agent
feature: todo-app
branch: phase/feature/webui-multitenant
user: unknown
command: implement-t005
labels:
  - tasks
  - api
files_yaml:
  - api/todo/routes/tasks.py
  - api/todo/main.py
tests_yaml: []
links:
  spec: specs/todo-app/spec.md
  plan: specs/todo-app/plan.md
  spike: specs/todo-app/spike-betterauth.md
---

PROMPT_TEXT:
"""
Implement Task T005 only.

Implement secure CRUD API endpoints for tasks
using FastAPI and SQLModel.

All endpoints must be protected by the existing
JWT auth middleware and scoped to the authenticated user.

Do NOT implement frontend or CI/CD.
"""

RESPONSE_TEXT:
"""
Added authenticated task CRUD endpoints at `/api/v1/tasks` (create, list, get, patch, delete). Endpoints use `require_current_user` to enforce JWT auth and scope DB queries to the token `sub` claim (parsed as UUID). No frontend or CI/CD changes were made. See `api/todo/routes/tasks.py`.
"""

OUTCOME: success
