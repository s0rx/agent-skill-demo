import json
import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import todo


def test_load_todos_returns_empty_list_when_file_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(todo, 'TODO_FILE', tmp_path / 'todos.json')
    assert todo.load_todos() == []


def test_load_todos_reads_valid_json(tmp_path, monkeypatch):
    file_path = tmp_path / 'todos.json'
    file_path.write_text(json.dumps([{'id': 1, 'text': 'task', 'done': False}]))
    monkeypatch.setattr(todo, 'TODO_FILE', file_path)
    assert todo.load_todos() == [{'id': 1, 'text': 'task', 'done': False}]


def test_load_todos_raises_json_decode_error_for_malformed_file(tmp_path, monkeypatch):
    file_path = tmp_path / 'todos.json'
    file_path.write_text('not valid json')
    monkeypatch.setattr(todo, 'TODO_FILE', file_path)
    with pytest.raises(json.JSONDecodeError):
        todo.load_todos()


def test_save_todos_writes_json_file(tmp_path, monkeypatch):
    file_path = tmp_path / 'todos.json'
    monkeypatch.setattr(todo, 'TODO_FILE', file_path)
    data = [{'id': 1, 'text': 'task', 'done': False}]
    todo.save_todos(data)
    assert json.loads(file_path.read_text()) == data


def test_add_todo_appends_todo_and_prints_message(tmp_path, monkeypatch, capsys):
    file_path = tmp_path / 'todos.json'
    monkeypatch.setattr(todo, 'TODO_FILE', file_path)

    class FixedDatetime:
        @classmethod
        def now(cls):
            return datetime(2020, 1, 1, 12, 0, 0)

    monkeypatch.setattr(todo, 'datetime', FixedDatetime)
    todo.add_todo('Buy milk')

    captured = capsys.readouterr()
    assert 'Added: Buy milk' in captured.out
    saved = json.loads(file_path.read_text())
    assert saved == [{
        'id': 1,
        'text': 'Buy milk',
        'done': False,
        'created': '2020-01-01T12:00:00',
    }]


def test_list_todos_prints_helpful_message_for_empty_list(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(todo, 'TODO_FILE', tmp_path / 'todos.json')
    todo.list_todos()
    captured = capsys.readouterr()
    assert 'No todos yet.' in captured.out


def test_list_todos_prints_completed_and_pending_items(tmp_path, monkeypatch, capsys):
    file_path = tmp_path / 'todos.json'
    todos = [
        {'id': 1, 'text': 'task1', 'done': False},
        {'id': 2, 'text': 'task2', 'done': True},
    ]
    file_path.write_text(json.dumps(todos))
    monkeypatch.setattr(todo, 'TODO_FILE', file_path)
    todo.list_todos()
    captured = capsys.readouterr()
    assert '[ ] 1. task1' in captured.out
    assert '[x] 2. task2' in captured.out


def test_done_todo_marks_item_completed_and_saves(tmp_path, monkeypatch, capsys):
    file_path = tmp_path / 'todos.json'
    todos = [{'id': 1, 'text': 'task1', 'done': False}]
    file_path.write_text(json.dumps(todos))
    monkeypatch.setattr(todo, 'TODO_FILE', file_path)

    todo.done_todo(1)
    captured = capsys.readouterr()
    assert 'Marked done: task1' in captured.out
    assert json.loads(file_path.read_text())[0]['done'] is True


def test_done_todo_reports_not_found_for_missing_id(tmp_path, monkeypatch, capsys):
    file_path = tmp_path / 'todos.json'
    file_path.write_text(json.dumps([{'id': 1, 'text': 'task1', 'done': False}]))
    monkeypatch.setattr(todo, 'TODO_FILE', file_path)

    todo.done_todo(2)
    captured = capsys.readouterr()
    assert 'Todo with id 2 not found' in captured.out


def test_main_dispatches_add_list_and_done_commands(tmp_path, monkeypatch, capsys):
    file_path = tmp_path / 'todos.json'
    monkeypatch.setattr(todo, 'TODO_FILE', file_path)

    class FixedDatetime:
        @classmethod
        def now(cls):
            return datetime(2020, 1, 1, 12, 0, 0)

    monkeypatch.setattr(todo, 'datetime', FixedDatetime)
    monkeypatch.setattr(sys, 'argv', ['todo.py', 'add', 'Hello'])
    todo.main()
    monkeypatch.setattr(sys, 'argv', ['todo.py', 'done', '1'])
    todo.main()
    captured = capsys.readouterr()

    assert 'Added: Hello' in captured.out
    assert 'Marked done: Hello' in captured.out
    monkeypatch.setattr(sys, 'argv', ['todo.py', 'list'])
    todo.main()
    captured = capsys.readouterr()
    assert '[x] 1. Hello' in captured.out


def test_main_reports_unknown_command(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(todo, 'TODO_FILE', tmp_path / 'todos.json')
    monkeypatch.setattr(sys, 'argv', ['todo.py', 'foobar'])
    todo.main()
    captured = capsys.readouterr()
    assert 'Unknown command: foobar' in captured.out
