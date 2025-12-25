```markdown
# Plan: Phase I — In‑Memory Todo Console App

**Source:** [specs/todo-app/spec.md](specs/todo-app/spec.md)

**Goal:** Deliver a Python 3.13+ console application that implements the five core todo features (add, view, mark complete/incomplete, update, delete) using in‑memory storage and a clear CLI.

## Architecture overview

- Style: small, layered CLI application following single‑responsibility principles.
- Layers:
  - Data Model: lightweight dataclasses for DTOs.
  - Repository: in‑memory storage with a simple CRUD API and auto‑increment ID.
  - Service / Use‑cases: validation, business rules, and repository orchestration.
  - UI / Controller: console menu loop, input parsing, presentation and error mapping.

## File structure

- `specs/todo-app/plan.md` — this plan.
- `README.md` — run and usage instructions.
- `main.py` — entrypoint; runs console loop.
- `todo/`
  - `__init__.py`
  - `models.py` — `Task` dataclass.
  - `repository.py` — `InMemoryTaskRepository` (add/get/update/delete/list).
  - `service.py` — `TaskService` (business logic, validations).
  - `ui.py` — console helpers and menu render/prompt functions.
  - `errors.py` — custom exceptions: `NotFoundError`, `ValidationError`.
- `tests/manual_checks.md` (optional) — manual acceptance checklist.

## Component responsibilities

- `Task` (`todo/models.py`)

  - Attributes: `id: int`, `title: str`, `description: Optional[str]`, `completed: bool` (defaults to `False`).
  - `id` assigned by repository; model is a simple DTO.

- `InMemoryTaskRepository` (`todo/repository.py`)

  - Maintains in‑memory dict/list and `next_id` counter.
  - Methods: `add(data) -> Task`, `get(id) -> Task`, `update(id, fields) -> Task`, `delete(id) -> None`, `list() -> list[Task]`.

- `TaskService` (`todo/service.py`)

  - Validates inputs (non‑empty titles), enforces business rules, calls repository methods.
  - Raises controlled exceptions (`ValidationError`, `NotFoundError`) for the UI to present.

- `UI` (`main.py` + `todo/ui.py`)

  - Presents a numbered menu: Add, View All, Update, Delete, Mark Complete/Incomplete, Quit.
  - Parses and validates user input safely and maps exceptions to friendly messages.

- `errors.py`
  - Small error types to enable clear control flow between service and UI.

## Execution flow (user journeys)

- Start: `python main.py` → welcome message and menu.
- Add task: UI prompts `Title` (non‑empty) and optional `Description` → `TaskService.create(...)` → repository assigns ID and stores → UI prints success.
- View all: `TaskService.list()` → UI formats rows `ID | [ ]/[x] | Title` or prints `No tasks yet.`
- Mark complete/incomplete: UI prompts `ID` and desired status (or toggles) → `TaskService.mark(id, completed)` → UI confirms.
- Update: UI prompts `ID` → fetches task → prompts new title/description (blank to keep) → `TaskService.update(...)` → UI shows updated task.
- Delete: UI prompts `ID`, asks for confirmation `Y/n` → `TaskService.delete(id)` → UI confirms removal.
- Errors: invalid ID or empty title produce friendly messages; app does not crash.

## Acceptance checks (mapped to spec)

- SC-001 (Functionality): Manual checklist in `tests/manual_checks.md` covering add/view/update/delete/mark.
- SC-002 (Input handling): Add/Update must reject empty titles; invalid IDs produce `No task with ID X` messages.
- SC-003 (Usability): Menu shows clear options and exits cleanly.

## Minimal API (signatures)

- `TaskService.create(title: str, description: Optional[str]) -> Task`
- `TaskService.list() -> list[Task]`
- `TaskService.get(id: int) -> Task`
- `TaskService.update(id: int, title: Optional[str], description: Optional[str]) -> Task`
- `TaskService.delete(id: int) -> None`
- `TaskService.mark(id: int, completed: bool) -> Task`

## Risks & mitigations

- Invalid user input causing crashes — centralize validation in `TaskService` and safe parsing in UI.
- User confusion with menu wording — use concise labels and short usage examples in `README.md`.
- Scope creep — lock Phase I to the five user stories; defer extras to Phase II.

## Next steps

1. Scaffold the project files (`todo/` package and `main.py`).
2. Implement `Task` and `InMemoryTaskRepository` (auto‑incrementing `id`).
3. Implement `TaskService` and `UI` with error handling.
4. Run manual acceptance checks listed in `tests/manual_checks.md`.

---

This plan implements the constraints and acceptance criteria in [specs/todo-app/spec.md](specs/todo-app/spec.md).
```
