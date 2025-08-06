from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy.orm import Session

from ..constants.error_messages import ERROR_MESSAGES
from ..domain.entities.task_entity import TaskEntity
from ..infrastructure.database.models import Task
from ..interfaces.task_repository_interface import ITaskRepository
from ._decorator import handle_db_errors


class TaskRepository(ITaskRepository):
    def __init__(self, session: Session):
        self.session = session
        
    @handle_db_errors
    def get_tasks(self, user_id):  # تصحيح كتابة self وتحديد نوع الإرجاع
        db_tasks = self.session.query(Task).filter(Task.user_id == user_id).all()
        return [self._convert_to_entity(task) for task in db_tasks]
        
    @handle_db_errors
    def create_task(self, task):
        db_task = Task(
            text=task.text,
            is_deleted=task.is_deleted if hasattr(task, 'is_deleted') else False,  # قيمة افتراضية
            is_completed=task.is_completed if hasattr(task, 'is_completed') else False,
            deleted_at=task.deleted_at if hasattr(task, 'deleted_at') else None,
            completed_at=task.completed_at if hasattr(task, 'completed_at') else None,
            due_at=task.due_at,
            created_at=task.created_at if hasattr(task, 'created_at') else datetime.now(timezone.utc),
            user_id=task.user_id,
            group_id=task.group_id if hasattr(task, 'group_id') else None
        )

        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)

        return self._convert_to_entity(db_task)

    @handle_db_errors
    def mark_task_completed(self, task_id, user_id):
        db_task = self.session.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id,
            Task.is_deleted == False  # أو Task.is_deleted.is_(False) حسب إصدار SQLAlchemy
        ).first()

        if not db_task:
            return None

        db_task.is_completed = True
        db_task.completed_at = datetime.now(timezone.utc)

        self.session.commit()
        self.session.refresh(db_task)

        return self._convert_to_entity(db_task)

    @handle_db_errors
    def mark_task_uncompleted(self, task_id, user_id):
        db_task = self.session.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id,
            Task.is_deleted == False
        ).first()

        if not db_task:
            return None

        db_task.is_completed = False
        db_task.completed_at = None

        self.session.commit()
        self.session.refresh(db_task)

        return self._convert_to_entity(db_task)

    @handle_db_errors
    def delete_task(self, task_id: int, user_id: int):
        db_task = self.session.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()

        if not db_task:
            return None

        db_task.is_deleted = True
        db_task.deleted_at = datetime.now(timezone.utc)

        self.session.commit()
        return True

    def _convert_to_entity(self, db_task):
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