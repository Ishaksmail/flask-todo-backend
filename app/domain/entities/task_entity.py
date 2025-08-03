# domain/entities/task_entity.py
from datetime import datetime, timezone
from typing import Optional


class TaskEntity:
    def __init__(self,
                 text: str,
                 is_deleted: bool = False,
                 is_completed: bool = False,
                 id: Optional[int]=None,
                 deleted_at: Optional[datetime] = None,
                 completed_at: Optional[datetime] = None,
                 due_at: Optional[datetime] = None,
                 created_at: Optional[datetime] = None,
                 user_id: Optional[int] = None,
                 group_id: Optional[int] = None):
        self.id = id
        self.text = text
        self.is_deleted = is_deleted
        self.is_completed = is_completed
        self.deleted_at = deleted_at
        self.completed_at = completed_at
        self.due_at = due_at
        self.created_at = created_at or datetime.now(timezone.utc)
        self.user_id = user_id
        self.group_id = group_id
