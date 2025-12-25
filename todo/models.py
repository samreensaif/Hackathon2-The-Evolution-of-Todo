from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __str__(self) -> str:
        status = "x" if self.completed else " "
        desc = f": {self.description}" if self.description else ""
        return f"{self.id} | [{status}] | {self.title}{desc}"
