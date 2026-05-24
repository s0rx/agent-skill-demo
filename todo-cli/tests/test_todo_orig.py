"""Tests for the Todo CLI application."""

from pathlib import Path
import pytest
import todo.cli as todo


@pytest.fixture(autouse=True)
def mock_todo_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Automatically redirect TODO_FILE to a temporary path for each test."""
    temp_file = tmp_path / "todos.json"
    monkeypatch.setattr(todo, "TODO_FILE", temp_file)
    return temp_file


def test_complete_todo(capsys: pytest.CaptureFixture[str]) -> None:
    """Test marking a todo as completed."""
    todo.save_todos([
        {
            "id": 1,
            "text": "Buy milk",
            "done": False,
            "created": "2026-05-24T20:00:00",
        }
    ])

    todo.complete_todo(1)

    captured = capsys.readouterr()
    assert "Completed: Buy milk" in captured.out

    todos = todo.load_todos()
    assert len(todos) == 1
    assert todos[0]["done"] is True


def test_complete_todo_not_found(capsys: pytest.CaptureFixture[str]) -> None:
    """Test marking a non-existent todo as completed."""
    todo.save_todos([])

    todo.complete_todo(1)

    captured = capsys.readouterr()
    assert "Error: Todo with ID 1 not found." in captured.out
