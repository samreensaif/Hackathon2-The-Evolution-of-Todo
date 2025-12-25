from typing import Optional, List
from .models import Task


def prompt_string(prompt: str, allow_empty: bool = False) -> str:
    while True:
        value = input(f"{prompt}").strip()
        if value or allow_empty:
            return value
        print("Input cannot be empty. Please try again.")


def prompt_optional_string(prompt: str) -> Optional[str]:
    value = input(f"{prompt} (leave empty to skip): ").strip()
    return value if value else None


def prompt_int(prompt: str) -> int:
    while True:
        value = input(f"{prompt}").strip()
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid integer.")


def confirm(prompt: str) -> bool:
    resp = input(f"{prompt} (y/N): ").strip().lower()
    return resp in ("y", "yes")


def format_task(task: Task) -> str:
    status = "x" if task.completed else " "
    desc = f" - {task.description}" if task.description else ""
    return f"{task.id:3} | [{status}] | {task.title}{desc}"


def format_task_list(tasks: List[Task]) -> str:
    if not tasks:
        return "No tasks yet."
    lines = [format_task(t) for t in tasks]
    return "\n".join(lines)
