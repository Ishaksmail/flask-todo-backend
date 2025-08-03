# domain/entities/group_entity.py
from datetime import datetime,timezone
from typing import Optional,List
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
