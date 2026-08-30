import json
import os
from typing import Any, Dict, List, Optional
from cli_todo.model import Todo

class TodoDatabase:
    def __init__(self, filename: str = 'todos.json'):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)
        
    def _raw_read(self) -> Dict[str, Any]:
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _raw_write(self, data: Dict[str, Any]) -> None:
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def get_next_id(self) -> int:
        data = self._raw_read()
        if not data:
            return 1
        return max(int(k) for k in data.keys()) + 1

    def save_single_task(self, todo: Todo):
        data = self._raw_read()
        data[todo.task_id] = todo.to_dict()
        self._raw_write(data)

    def get_all_tasks(self) -> List[Todo]:
        data = self._raw_read()
        todos = [Todo.from_dict(v) for v in data.values()]
        return sorted(todos, key=lambda t: t.task_id, reverse=True)

    def get_task_by_id(self, task_id: int) -> Optional[Todo]:
        data = self._raw_read()
        task_data = data.get(str(task_id))
        if task_data:
            return Todo.from_dict(task_data)
        return None

    def delete_task_by_id(self, task_id: int) -> bool:
        data = self._raw_read()
        if str(task_id) in data:
            del data[str(task_id)]
            self._raw_write(data)
            return True
        return False