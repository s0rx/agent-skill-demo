"""Todo CLI Package.

Exposes the core functions of the CLI application for imports.
"""

from todo.cli import (
    main,
    load_todos,
    save_todos,
    add_todo,
    list_todos,
    complete_todo,
)

__all__ = [
    "main",
    "load_todos",
    "save_todos",
    "add_todo",
    "list_todos",
    "complete_todo",
]
