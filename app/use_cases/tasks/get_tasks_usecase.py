from typing import List
from ...domain.entities.task_entity import TaskEntity
from ...interfaces.task_repository_interface import ITaskRepository
from ...constants.error_messages import ERROR_MESSAGES


class GetTaskUseCase:
    def __init__(self, task_repository: ITaskRepository):
        self.task_repository = task_repository

    def get_all_tasks(self, user_id: int) -> List[TaskEntity]:
      
        if not user_id:
            raise ValueError(ERROR_MESSAGES["USER_ID_REQUIRED"])

        return self.task_repository.get_tasks(user_id=user_id)
