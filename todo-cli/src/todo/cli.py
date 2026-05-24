"""Command-line interface logic for the Todo CLI application."""

import json
import sys
from datetime import datetime
from pathlib import Path

TODO_FILE = Path("todos.json")


def load_todos():
    if not TODO_FILE.exists():
        return []
    return json.loads(TODO_FILE.read_text())


def save_todos(todos):
    TODO_FILE.write_text(json.dumps(todos, indent=2))


def add_todo(text):
    todos = load_todos()
    todos.append({
        "id": len(todos) + 1,
        "text": text,
        "done": False,
        "created": datetime.now().isoformat(timespec="seconds"),
    })
    save_todos(todos)
    print(f"Added: {text}")


def list_todos():
    todos = load_todos()
    if not todos:
        print('No todos yet. Add one with: python -m todo add "your task"')
        return
    for t in todos:
        mark = "[x]" if t["done"] else "[ ]"
        print(f"{mark} {t['id']}. {t['text']}")


def complete_todo(todo_id: int) -> None:
    """Mark a todo item as completed by its ID."""
    todos = load_todos()
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = True
            save_todos(todos)
            print(f"Completed: {t['text']}")
            return
    print(f"Error: Todo with ID {todo_id} not found.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m todo [add <text> | list | done <id>]")
        return
    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) > 2:
        add_todo(" ".join(sys.argv[2:]))
    elif cmd == "list":
        list_todos()
    elif cmd == "done":
        if len(sys.argv) > 2:
            try:
                todo_id = int(sys.argv[2])
                complete_todo(todo_id)
            except ValueError:
                print("Error: ID must be an integer.")
        else:
            print("Usage: python -m todo done <id>")
    else:
        print(f"Unknown command: {cmd}")
