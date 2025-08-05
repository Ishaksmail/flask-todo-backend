from typing import List
from ...domain.entities.group_entity import GroupEntity
from ...interfaces.group_repository_interface import IGroupRepository
from ...constants.error_messages import ERROR_MESSAGES


class GetGroupUseCase:
    def __init__(self, group_repo: IGroupRepository):
        self.group_repo = group_repo

    def get_all_groups(self, user_id: int) -> List[GroupEntity]:
      
        if not user_id:
            raise ValueError(ERROR_MESSAGES["USER_ID_REQUIRED"])

        return self.group_repo.get_groups(user_id=user_id)

    def get_completed_groups(self, user_id: int) -> List[GroupEntity]:
       
        if not user_id:
            raise ValueError(ERROR_MESSAGES["USER_ID_REQUIRED"])

        return self.group_repo.get_groups_complete(user_id=user_id)

    def get_uncompleted_groups(self, user_id: int) -> List[GroupEntity]:
        
        if not user_id:
            raise ValueError(ERROR_MESSAGES["USER_ID_REQUIRED"])

        return self.group_repo.get_groups_uncomplete(user_id=user_id)
