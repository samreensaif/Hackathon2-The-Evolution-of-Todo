---
id: 0006
title: Phase II Speckit Tasks
stage: tasks
date_iso: 2025-12-25
surface: agent
model: agent
feature: todo-app
branch: phase/feature/webui-multitenant
user: unknown
command: create-tasks
labels:
  - tasks
  - phase-ii
files_yaml:
  - specs/todo-app/tasks.md
tests_yaml: []
links:
  spec: specs/todo-app/spec.md
  plan: specs/todo-app/plan.md
  adr: null
  pr: null
---

PROMPT_TEXT:
"""
Based on the updated Phase II spec.md and plan.md,
create speckit.tasks for Phase II.

Break the plan into small, atomic, sequential tasks
suitable for spec-driven implementation.

Do NOT write any code.
Only create tasks.
"""

RESPONSE_TEXT:
"""
Created `specs/todo-app/tasks.md` with atomic Phase II tasks grouped by sprint and cross‑cutting tasks. Tasks include descriptions, acceptance criteria, and dependencies. No code written.
"""

OUTCOME: success
