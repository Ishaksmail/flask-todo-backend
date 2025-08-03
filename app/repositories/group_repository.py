from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from ..interfaces.group_repository_interface import IGroupRepository
from ..infrastructure.database.models import Group, Task
from ..domain.entities.group_entity import GroupEntity
from ..domain.entities.task_entity import TaskEntity

class GroupRepository(IGroupRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def get_groups(self, user_id: int) -> List[GroupEntity]:
        
        db_groups = self.session.query(Group).filter(
            Group.user_id == user_id,
            Group.is_deleted == False
        ).order_by(Group.created_at.desc()).all()
        
        return [self._convert_to_group_entity(group) for group in db_groups]

    def get_groups_uncomplete(self, user_id: int) -> List[GroupEntity]:
        
        db_groups = self.session.query(Group).filter(
            Group.user_id == user_id,
            Group.is_deleted == False,
            Group.tasks.any(
                Task.is_completed == False,
                Task.is_deleted == False
            )
        ).order_by(Group.created_at.desc()).all()
        
        return [self._convert_to_group_entity(group, include_tasks=True) for group in db_groups]

    def get_groups_complete(self, user_id: int) -> List[GroupEntity]:
        
        db_groups = self.session.query(Group).filter(
            Group.user_id == user_id,
            Group.is_deleted == False,
            ~Group.tasks.any(
                Task.is_completed == False,
                Task.is_deleted == False
            )
        ).order_by(Group.created_at.desc()).all()
        
        return [self._convert_to_group_entity(group, include_tasks=True) for group in db_groups]

    def create_group(self, group: GroupEntity) -> GroupEntity:
        
      
        db_group = Group(
            name=group.name,
            description=group.description,
            user_id=group.user_id,
            created_at=group.created_at or datetime.utcnow()
        )
        
        self.session.add(db_group)
        self.session.commit()
        self.session.refresh(db_group)
        
        return self._convert_to_group_entity(db_group)

    def update_group(self, group: GroupEntity) -> Optional[GroupEntity]:
      
        db_group = self.session.query(Group).filter(
            Group.id == group.id,
            Group.is_deleted == False
        ).first()
        
        if not db_group:
            return None
            
        db_group.name = group.name
        db_group.description = group.description
        db_group.updated_at = datetime.utcnow()
        
        self.session.commit()
        return self._convert_to_group_entity(db_group)

    def delete_group(self, group_id: int) -> bool:
       
        db_group = self.session.query(Group).filter(
            Group.id == group_id,
            Group.is_deleted == False
        ).first()
        
        if not db_group:
            return False
            
        db_group.is_deleted = True
        db_group.deleted_at = datetime.utcnow()
        
        for task in db_group.tasks:
            task.is_deleted = True
            task.deleted_at = datetime.utcnow()
        
        self.session.commit()
        return True
    
    # الدوال المساعدة
    def _convert_to_task_entity(self, db_task: Task) -> TaskEntity:
       
        return TaskEntity(
            id=db_task.id,
            text=db_task.text,
            is_deleted=db_task.is_deleted,
            is_completed=db_task.is_completed,
            deleted_at=db_task.deleted_at,
            completed_at=db_task.completed_at,
            due_at=db_task.due_at,
            created_at=db_task.created_at,
            user_id=db_task.user_id,
            group_id=db_task.group_id
        )

    def _convert_to_group_entity(self, db_group: Group, include_tasks: bool = False) -> GroupEntity:
        
        tasks = []
        if include_tasks:
            tasks = [
                self._convert_to_task_entity(task) 
                for task in db_group.tasks 
                if not task.is_deleted
            ]
        
        return GroupEntity(
            id=db_group.id,
            name=db_group.name,
            description=db_group.description,
            is_deleted=db_group.is_deleted,
            deleted_at=db_group.deleted_at,
            created_at=db_group.created_at,
            updated_at=db_group.updated_at,
            user_id=db_group.user_id,
            tasks=tasks
        )