from typing import List, Optional, Protocol

from ..domain.entities.group_entity import GroupEntity
from ..domain.entities.task_entity import TaskEntity
from ..infrastructure.database.models import Group, Task


class IGroupRepository(Protocol):

    def get_groups(self, user_id: int) -> List[GroupEntity]:
        ...

    def get_groups_uncomplete(self, user_id: int) -> List[GroupEntity]:
        ...

    def get_groups_complete(self, user_id: int) -> List[GroupEntity]:
        ...

    def create_group(self, group: GroupEntity) -> GroupEntity:
        ...

    def update_group(self,group: GroupEntity) -> Optional[GroupEntity]:
        ...

    def delete_group(self, group_id: int) -> bool:
        ...
    
    # helper
    
    def _convert_to_task_entity(self, db_task: Task) -> TaskEntity:
        ...
    
    def _convert_to_group_entity(self, db_group: Group, include_tasks: bool = False) -> GroupEntity:
        ...