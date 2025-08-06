from ...domain.entities.task_entity import TaskEntity
from ...repositories.task_repository import TaskRepository
from datetime import datetime, timezone


class CreateTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, text: str, user_id: int, group_id: int = None, due_at=None):
        # إنشاء كيان المهمة
        task = TaskEntity(
            id=None,
            text=text,
            is_deleted=False,
            is_completed=False,
            deleted_at=None,
            completed_at=None,
            due_at=due_at,
            created_at=datetime.now(timezone.utc),
            user_id=user_id,
            group_id=group_id
        )
        
        # استدعاء المستودع لحفظ المهمة
        return self.task_repository.create_task(task)
