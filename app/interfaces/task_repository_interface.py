from typing import List, Optional, Protocol

from app.domain.entities.task_entity import TaskEntity
from app.infrastructure.database.models import Task


class ITaskRepository(Protocol):
    
    def get_tasks(slef, user_id: int) -> List[TaskEntity] :
        ...
                
    def create_task(self, task: TaskEntity,user_id: int) -> TaskEntity:
        ...

    def mark_task_completed(self, task_id: int,user_id: int) -> Optional[TaskEntity]:
        ...

    def mark_task_uncompleted(self, task_id: int,user_id: int) -> Optional[TaskEntity]:
        ...

    def delete_task(self, task_id: int,user_id: int) -> bool:
        ...
        
    # helper
    
    def _convert_to_entity (self,db_task: Task) -> TaskEntity :
        ...
