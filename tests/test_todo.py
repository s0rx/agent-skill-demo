import json
import todo


def test_load_todos_missing_file(tmp_path, monkeypatch):
    """Returns empty list if file doesn't exist."""
    d = tmp_path / "subdir"
    d.mkdir()
    f = d / "todos.json"
    monkeypatch.setattr(todo, "TODO_FILE", f)
    assert todo.load_todos() == []


def test_load_todos_existing_file(tmp_path, monkeypatch):
    """Returns list if file exists."""
    f = tmp_path / "todos.json"
    data = [{"id": 1, "text": "test", "done": False}]
    f.write_text(json.dumps(data))
    monkeypatch.setattr(todo, "TODO_FILE", f)
    assert todo.load_todos() == data


def test_save_todos(tmp_path, monkeypatch):
    """Correctly saves list to file."""
    f = tmp_path / "todos.json"
    monkeypatch.setattr(todo, "TODO_FILE", f)
    data = [{"id": 1, "text": "saved", "done": True}]
    todo.save_todos(data)
    assert json.loads(f.read_text()) == data


def test_add_todo(tmp_path, monkeypatch):
    """Adds a todo item correctly."""
    f = tmp_path / "todos.json"
    monkeypatch.setattr(todo, "TODO_FILE", f)
    todo.add_todo("New task")
    todos = todo.load_todos()
    assert len(todos) == 1
    assert todos[0]["text"] == "New task"
    assert todos[0]["done"] is False
    assert "created" in todos[0]


def test_list_todos_empty(capsys, tmp_path, monkeypatch):
    """Prints help message when no todos exist."""
    monkeypatch.setattr(todo, "TODO_FILE", tmp_path / "empty.json")
    todo.list_todos()
    captured = capsys.readouterr()
    assert "No todos yet" in captured.out


def test_list_todos_filled(capsys, tmp_path, monkeypatch):
    """Prints todos in list."""
    f = tmp_path / "todos.json"
    data = [{"id": 1, "text": "Task 1", "done": False},
            {"id": 2, "text": "Task 2", "done": True}]
    f.write_text(json.dumps(data))
    monkeypatch.setattr(todo, "TODO_FILE", f)
    todo.list_todos()
    captured = capsys.readouterr()
    assert "[ ] 1. Task 1" in captured.out
    assert "[x] 2. Task 2" in captured.out


def test_done_todo_success(capsys, tmp_path, monkeypatch):
    """Marks a todo as done."""
    f = tmp_path / "todos.json"
    data = [{"id": 1, "text": "Task 1", "done": False}]
    f.write_text(json.dumps(data))
    monkeypatch.setattr(todo, "TODO_FILE", f)
    todo.done_todo(1)
    todos = todo.load_todos()
    assert todos[0]["done"] is True
    captured = capsys.readouterr()
    assert "Marked done: Task 1" in captured.out


def test_done_todo_not_found(capsys, tmp_path, monkeypatch):
    """Handles missing ID for done."""
    monkeypatch.setattr(todo, "TODO_FILE", tmp_path / "none.json")
    todo.done_todo(99)
    captured = capsys.readouterr()
    assert "Todo with id 99 not found" in captured.out


def test_drop_todo_success(capsys, tmp_path, monkeypatch):
    """Removes a todo."""
    f = tmp_path / "todos.json"
    data = [{"id": 1, "text": "Task 1", "done": False}]
    f.write_text(json.dumps(data))
    monkeypatch.setattr(todo, "TODO_FILE", f)
    todo.drop_todo(1)
    assert len(todo.load_todos()) == 0
    captured = capsys.readouterr()
    assert "Dropped todo with id 1" in captured.out


def test_main_routing_add(tmp_path, monkeypatch):
    """Main routes to add_todo."""
    f = tmp_path / "todos.json"
    monkeypatch.setattr(todo, "TODO_FILE", f)
    monkeypatch.setattr("sys.argv",
                        ["todo.py", "add", "Bread", "and", "Butter"])
    todo.main()
    todos = todo.load_todos()
    assert todos[0]["text"] == "Bread and Butter"


def test_main_routing_invalid_id(capsys, monkeypatch):
    """Main handles invalid ID gracefully."""
    monkeypatch.setattr("sys.argv", ["todo.py", "done", "abc"])
    todo.main()
    captured = capsys.readouterr()
    assert "is not a valid todo ID" in captured.out
