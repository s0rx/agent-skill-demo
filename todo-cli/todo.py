"""Simple Todo CLI.

A starter project to practice using AI coding assistants.

Usage:
    python todo.py add "Buy milk"
    python todo.py list
"""

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
        print('No todos yet. Add one with: python todo.py add "your task"')
        return
    for t in todos:
        mark = "[x]" if t["done"] else "[ ]"
        print(f"{mark} {t['id']}. {t['text']}")


def done_todo(todo_id):
    """Mark a todo as completed by ID."""
    todos = load_todos()
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = True
            save_todos(todos)
            print(f"Marked done: {t['text']}")
            return
    print(f"Todo with id {todo_id} not found")


def main():
    if len(sys.argv) < 2:
        print("Usage: python todo.py [add <text> | list | done <id>]")
        return
    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) > 2:
        add_todo(" ".join(sys.argv[2:]))
    elif cmd == "list":
        list_todos()
    elif cmd == "done" and len(sys.argv) > 2:
        try:
            todo_id = int(sys.argv[2])
            done_todo(todo_id)
        except ValueError:
            print(f"Error: '{sys.argv[2]}' is not a valid todo ID")
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
