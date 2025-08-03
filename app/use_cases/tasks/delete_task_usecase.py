from ...interfaces.task_repository_interface import ITaskRepository


class DeleteTaskUseCase:
    def __init__(self, task_repository: ITaskRepository):
        self.task_repository = task_repository

    def execute(self, task_id: int, user_id: int) -> bool:
        
        return self.task_repository.delete_task(task_id, user_id)
