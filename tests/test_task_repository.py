# tests/test_task_repository.py
from app.repositories.task_repository import TaskRepository
from app.domain.entities.task_entity import TaskEntity

def test_create_and_complete_task(db_session):
    repo = TaskRepository(db_session)
    task = TaskEntity(
        id=None,
        text="Test task",
        is_deleted=False,
        is_completed=False,
        deleted_at=None,
        completed_at=None,
        due_at=None,
        created_at=None,
        user_id=1,
        group_id=None
    )
    created_task = repo.create_task(task)
    assert created_task.id is not None

    # تحديد المهمة كمكتملة
    updated_task = repo.mark_task_completed(created_task.id, 1)
    assert updated_task.is_completed is True

def test_delete_task(db_session):
    repo = TaskRepository(db_session)
    task = TaskEntity(
        id=None,
        text="Task to delete",
        is_deleted=False,
        is_completed=False,
        deleted_at=None,
        completed_at=None,
        due_at=None,
        created_at=None,
        user_id=1,
        group_id=None
    )
    created_task = repo.create_task(task)
    result = repo.delete_task(created_task.id, 1)
    assert result is True
