---
id: 0011
title: Implement T006 — JWT Auth Middleware
stage: tasks
date_iso: 2025-12-25
surface: agent
model: agent
feature: todo-app
branch: phase/feature/webui-multitenant
user: unknown
command: implement-t006
labels:
  - tasks
  - auth
files_yaml:
  - api/pyproject.toml
  - api/todo/auth.py
  - api/todo/main.py
tests_yaml: []
links:
  spec: specs/todo-app/spec.md
  plan: specs/todo-app/plan.md
  spike: specs/todo-app/spike-betterauth.md
---

PROMPT_TEXT:
"""
Implement Task T006 only.

Implement JWT authentication middleware for FastAPI
based on the BetterAuth spike document.

Do NOT implement CRUD API endpoints yet.
Do NOT modify frontend.
"""

RESPONSE_TEXT:
"""
Added JWT verification helpers (`api/todo/auth.py`) using `python-jose`, updated `api/pyproject.toml`, and added a FastAPI middleware wrapper in `api/todo/main.py` that sets `request.state.current_user` when a valid Bearer token is provided. Middleware does not enforce authentication by itself; endpoints may use `require_current_user` dependency when they require auth. No CRUD endpoints or frontend changes were made.
"""

OUTCOME: success
