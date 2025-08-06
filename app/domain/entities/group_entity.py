from datetime import datetime
from typing import List, Optional
from .task_entity import TaskEntity


class GroupEntity:
    def __init__(self,
                 name: str,
                 description: Optional[str] = None,
                 is_deleted: bool = False,
                 id: Optional[int]=None,
                 deleted_at: Optional[datetime] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None,
                 user_id: Optional[int] = None,
                 tasks: Optional[List[TaskEntity]] = None
                 ):
        
        self.id = id
        self.name = name
        self.description = description
        self.is_deleted = is_deleted
        self.deleted_at = deleted_at
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at
        self.user_id = user_id
        self.tasks = tasks or []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_deleted": self.is_deleted,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id,
            "tasks": [task.to_dict() for task in self.tasks] if self.tasks else []
        }
