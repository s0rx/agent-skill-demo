"""Tests for the Todo CLI application."""

import runpy
import sys
from pathlib import Path
import pytest
import todo.cli as todo


@pytest.fixture(autouse=True)
def mock_todo_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Automatically redirect TODO_FILE to a temporary path for each test."""
    temp_file = tmp_path / "todos.json"
    monkeypatch.setattr(todo, "TODO_FILE", temp_file)
    return temp_file


def test_load_todos_empty() -> None:
    """Test load_todos when the file does not exist."""
    assert todo.load_todos() == []


def test_load_todos_existing() -> None:
    """Test load_todos when the file contains valid JSON data."""
    todo.save_todos([{"id": 1, "text": "Task 1", "done": False}])
    loaded = todo.load_todos()
    assert len(loaded) == 1
    assert loaded[0]["text"] == "Task 1"


def test_save_todos() -> None:
    """Test save_todos writes data correctly to the file."""
    todos = [{"id": 1, "text": "Task 1", "done": False}]
    todo.save_todos(todos)
    assert todo.load_todos() == todos


def test_add_todo(capsys: pytest.CaptureFixture[str]) -> None:
    """Test adding a todo item updates the file and prints confirmation."""
    todo.add_todo("Buy milk")
    captured = capsys.readouterr()
    assert "Added: Buy milk" in captured.out

    todos = todo.load_todos()
    assert len(todos) == 1
    assert todos[0]["text"] == "Buy milk"
    assert todos[0]["id"] == 1
    assert todos[0]["done"] is False
    assert "created" in todos[0]


def test_list_todos_empty(capsys: pytest.CaptureFixture[str]) -> None:
    """Test list_todos when there are no todo items."""
    todo.list_todos()
    captured = capsys.readouterr()
    assert "No todos yet" in captured.out


def test_list_todos(capsys: pytest.CaptureFixture[str]) -> None:
    """Test listing todo items displays them with correct checkmarks."""
    todo.save_todos([
        {"id": 1, "text": "Task 1", "done": False},
        {"id": 2, "text": "Task 2", "done": True},
    ])
    todo.list_todos()
    captured = capsys.readouterr()
    assert "[ ] 1. Task 1" in captured.out
    assert "[x]" in captured.out and "2. Task 2" in captured.out


def test_complete_todo(capsys: pytest.CaptureFixture[str]) -> None:
    """Test complete_todo marks task as completed."""
    todo.save_todos([{"id": 1, "text": "Task 1", "done": False}])
    todo.complete_todo(1)
    captured = capsys.readouterr()
    assert "Completed: Task 1" in captured.out

    todos = todo.load_todos()
    assert todos[0]["done"] is True


def test_complete_todo_not_found(capsys: pytest.CaptureFixture[str]) -> None:
    """Test complete_todo prints error when task is not found."""
    todo.complete_todo(99)
    captured = capsys.readouterr()
    assert "Error: Todo with ID 99 not found." in captured.out


def test_main_no_args(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main function displays usage when run without arguments."""
    monkeypatch.setattr(sys, "argv", ["todo"])
    todo.main()
    captured = capsys.readouterr()
    assert "Usage: python -m todo" in captured.out


def test_main_unknown_command(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main function handling of unknown commands."""
    monkeypatch.setattr(sys, "argv", ["todo", "unknown"])
    todo.main()
    captured = capsys.readouterr()
    assert "Unknown command: unknown" in captured.out


def test_main_add(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main function adds a new todo task."""
    monkeypatch.setattr(sys, "argv", ["todo", "add", "Buy", "milk"])
    todo.main()
    captured = capsys.readouterr()
    assert "Added: Buy milk" in captured.out


def test_main_list(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main function lists todo tasks."""
    todo.save_todos([{"id": 1, "text": "Task 1", "done": False}])
    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    todo.main()
    captured = capsys.readouterr()
    assert "1. Task 1" in captured.out


def test_main_done(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main function completes a todo task."""
    todo.save_todos([{"id": 1, "text": "Task 1", "done": False}])
    monkeypatch.setattr(sys, "argv", ["todo", "done", "1"])
    todo.main()
    captured = capsys.readouterr()
    assert "Completed: Task 1" in captured.out


def test_main_done_invalid_id(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main function reports error for non-integer ID."""
    monkeypatch.setattr(sys, "argv", ["todo", "done", "abc"])
    todo.main()
    captured = capsys.readouterr()
    assert "Error: ID must be an integer." in captured.out


def test_main_done_missing_id(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test main function reports usage for missing ID."""
    monkeypatch.setattr(sys, "argv", ["todo", "done"])
    todo.main()
    captured = capsys.readouterr()
    assert "Usage: python -m todo done <id>" in captured.out


def test_main_module(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test running the package directly via __main__ entrypoint."""
    monkeypatch.setattr(sys, "argv", ["todo", "list"])
    todo.save_todos([])
    runpy.run_module("todo", run_name="__main__")
    captured = capsys.readouterr()
    assert "No todos yet" in captured.out
