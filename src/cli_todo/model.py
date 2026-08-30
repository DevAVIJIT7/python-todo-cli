from datetime import datetime
from typing import Dict, Any

class Todo:
    def __init__(self, title: str, task_id: str, completed: bool = False):
        self.task_id = task_id
        self.title = title
        self.completed = completed
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.created_at = current_time
        self.updated_at = current_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def update(self, title: str | None = None, completed: bool | None = None):
        if title is not None:
            self.title = title
        if completed is not None:
            self.completed = completed
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Todo":
        return cls(
            title=data["title"],
            task_id=data["task_id"],
            completed=data.get("completed", False)
        )