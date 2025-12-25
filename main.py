"""Entrypoint for the In‑Memory Todo Console App."""
from todo.service import TaskService
from todo import ui
from todo.errors import ValidationError, NotFoundError


def print_menu() -> None:
    print("\n== Todo App ==")
    print("1) Add task")
    print("2) View all tasks")
    print("3) Update task")
    print("4) Delete task")
    print("5) Mark complete/incomplete")
    print("6) Quit")


def main() -> None:
    service = TaskService()
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            try:
                title = ui.prompt_string("Title: ")
                description = ui.prompt_optional_string("Description")
                task = service.create(title, description)
                print(f"Task added: {task}")
            except ValidationError as e:
                print(f"Error: {e}")
        elif choice == "2":
            tasks = service.list()
            print(ui.format_task_list(tasks))
        elif choice == "3":
            try:
                task_id = ui.prompt_int("Task ID to update: ")
                title = ui.prompt_optional_string("New Title")
                description = ui.prompt_optional_string("New Description")
                task = service.update(task_id, title=title, description=description)
                print(f"Updated: {task}")
            except (ValidationError, NotFoundError) as e:
                print(f"Error: {e}")
        elif choice == "4":
            try:
                task_id = ui.prompt_int("Task ID to delete: ")
                if ui.confirm("Confirm delete?"):
                    service.delete(task_id)
                    print("Task deleted.")
            except NotFoundError as e:
                print(f"Error: {e}")
        elif choice == "5":
            try:
                task_id = ui.prompt_int("Task ID to mark: ")
                status_in = input("Mark as complete? (y/N): ").strip().lower()
                completed = status_in in ("y", "yes")
                task = service.mark(task_id, completed=completed)
                print(f"Updated: {task}")
            except NotFoundError as e:
                print(f"Error: {e}")
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please select a menu option.")


if __name__ == "__main__":
    main()
