from typing import Dict, List, Optional
from .models import Task
from .errors import NotFoundError


class InMemoryTaskRepository:
    """Simple in-memory repository for Task objects.

    Responsibility: store and retrieve Task instances, provide auto-incrementing ids.
    """

    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, title: str, description: Optional[str] = None) -> Task:
        task = Task(id=self._next_id, title=title, description=description, completed=False)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task:
        try:
            return self._tasks[task_id]
        except KeyError:
            raise NotFoundError(f"Task with id {task_id} not found")

    def update(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Task:
        task = self.get(task_id)
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        return task

    def delete(self, task_id: int) -> None:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return
        raise NotFoundError(f"Task with id {task_id} not found")

    def list(self) -> List[Task]:
        return list(self._tasks.values())
