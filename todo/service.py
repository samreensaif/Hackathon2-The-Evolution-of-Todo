from typing import List, Optional
from .repository import InMemoryTaskRepository
from .errors import ValidationError, NotFoundError
from .models import Task


class TaskService:
    """Business logic layer for tasks.

    Responsibilities: validate input, orchestrate repository calls, and raise controlled errors.
    """

    def __init__(self, repo: Optional[InMemoryTaskRepository] = None) -> None:
        self.repo = repo or InMemoryTaskRepository()

    def create(self, title: str, description: Optional[str] = None) -> Task:
        if not title or not title.strip():
            raise ValidationError("Title must not be empty")
        return self.repo.add(title=title.strip(), description=description)

    def list(self) -> List[Task]:
        return self.repo.list()

    def get(self, task_id: int) -> Task:
        return self.repo.get(task_id)

    def update(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        if title is not None and not title.strip():
            raise ValidationError("Title must not be empty")
        return self.repo.update(task_id, title=title.strip() if title is not None else None, description=description)

    def delete(self, task_id: int) -> None:
        self.repo.delete(task_id)

    def mark(self, task_id: int, completed: bool) -> Task:
        return self.repo.update(task_id, completed=completed)
