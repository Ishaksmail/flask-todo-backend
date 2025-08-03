from ...interfaces.task_repository_interface import ITaskRepository
from ...domain.entities.task_entity import TaskEntity


class MarkTaskUncompletedUseCase:
    def __init__(self, task_repository: ITaskRepository):
        self.task_repository = task_repository

    def execute(self, task_id: int, user_id: int) -> TaskEntity | None:
        return self.task_repository.mark_task_uncompleted(task_id, user_id)
