import json
import pytest
import todo
from datetime import datetime


def test_main_no_args_prints_usage(capsys, monkeypatch):
    """Main prints usage when no arguments provided."""
    monkeypatch.setattr("sys.argv", ["todo.py"])
    todo.main()
    captured = capsys.readouterr()
    assert "Usage: python todo.py" in captured.out


def test_main_unknown_command(capsys, monkeypatch):
    """Unknown command is reported to the user."""
    monkeypatch.setattr("sys.argv", ["todo.py", "foobar"])
    todo.main()
    captured = capsys.readouterr()
    assert "Unknown command: foobar" in captured.out


def test_add_todo_prints_and_saves(tmp_path, monkeypatch, capsys):
    """Adding a todo prints confirmation and persists the item."""
    f = tmp_path / "todos.json"
    monkeypatch.setattr(todo, "TODO_FILE", f)
    todo.add_todo("Say hello")
    captured = capsys.readouterr()
    assert "Added: Say hello" in captured.out
    data = json.loads(f.read_text())
    assert data[0]["text"] == "Say hello"


def test_drop_todo_not_found(capsys, tmp_path, monkeypatch):
    """Dropping a non-existent id prints a not-found message."""
    monkeypatch.setattr(todo, "TODO_FILE", tmp_path / "none.json")
    todo.drop_todo(42)
    captured = capsys.readouterr()
    assert "Todo with id 42 not found" in captured.out


def test_load_todos_malformed_raises(tmp_path, monkeypatch):
    """load_todos raises JSONDecodeError on malformed file."""
    f = tmp_path / "todos.json"
    f.write_text("not a json")
    monkeypatch.setattr(todo, "TODO_FILE", f)
    with pytest.raises(json.JSONDecodeError):
        todo.load_todos()


def test_save_todos_non_serializable_raises(tmp_path, monkeypatch):
    """save_todos raises when given non-serializable objects."""
    f = tmp_path / "todos.json"
    monkeypatch.setattr(todo, "TODO_FILE", f)
    data = [{"id": 1, "text": "x", "done": False, "created": datetime.now()}]
    with pytest.raises(TypeError):
        todo.save_todos(data)


def test_add_todo_empty_text(tmp_path, monkeypatch):
    """Adding an empty text todo is allowed and stored."""
    f = tmp_path / "todos.json"
    monkeypatch.setattr(todo, "TODO_FILE", f)
    todo.add_todo("")
    todos = todo.load_todos()
    assert len(todos) == 1
    assert todos[0]["text"] == ""


def test_add_todo_increment_ids(tmp_path, monkeypatch):
    """IDs increment based on existing todos in file."""
    f = tmp_path / "todos.json"
    existing = [{"id": 1, "text": "one", "done": False, "created":
                 "2020-01-01T00:00:00"}]
    f.write_text(json.dumps(existing))
    monkeypatch.setattr(todo, "TODO_FILE", f)
    todo.add_todo("second")
    todos = todo.load_todos()
    assert len(todos) == 2
    assert todos[1]["id"] == 2


def test_add_todo_uses_datetime_iso(tmp_path, monkeypatch):
    """add_todo records created time using datetime.now().isoformat."""
    f = tmp_path / "todos.json"
    monkeypatch.setattr(todo, "TODO_FILE", f)
    fixed = datetime(2020, 5, 4, 12, 30, 15)

    class DummyDT:
        @staticmethod
        def now():
            return fixed

    monkeypatch.setattr(todo, "datetime", DummyDT)
    todo.add_todo("timed")
    todos = todo.load_todos()
    assert todos[0]["created"] == fixed.isoformat(timespec="seconds")


def test_main_no_args_prints_usage_(capsys, monkeypatch):
    """main prints usage when no command provided."""
    monkeypatch.setattr("sys.argv", ["todo.py"])
    todo.main()
    captured = capsys.readouterr()
    assert "Usage: python todo.py" in captured.out


def test_main_unknown_command_(capsys, monkeypatch):
    """Unknown command is reported to the user."""
    monkeypatch.setattr("sys.argv", ["todo.py", "wat"])
    todo.main()
    captured = capsys.readouterr()
    assert "Unknown command: wat" in captured.out


def test_drop_todo_not_found_(capsys, tmp_path, monkeypatch):
    """drop_todo prints not found when ID missing."""
    monkeypatch.setattr(todo, "TODO_FILE", tmp_path / "no.json")
    todo.drop_todo(5)
    captured = capsys.readouterr()
    assert "Todo with id 5 not found" in captured.out
