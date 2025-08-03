from typing import List
from app.domain.entities.group_entity import GroupEntity
from app.interfaces.group_repository_interface import IGroupRepository


class GetGroupUseCase:
    def __init__(self, group_repo: IGroupRepository):
        self.group_repo = group_repo

    def get_all_groups(self, user_id: int) -> List[GroupEntity]:
        """Retrieve all groups for a specific user"""
        if not user_id:
            raise ValueError("User ID is required")

        groups = self.group_repo.get_groups(user_id=user_id)
        return groups

    def get_completed_groups(self, user_id: int) -> List[GroupEntity]:
        """Retrieve only completed groups for a specific user"""
        if not user_id:
            raise ValueError("User ID is required")

        groups = self.group_repo.get_groups_complete(user_id=user_id)
        return groups

    def get_uncompleted_groups(self, user_id: int) -> List[GroupEntity]:
        """Retrieve only uncompleted groups for a specific user"""
        if not user_id:
            raise ValueError("User ID is required")

        groups = self.group_repo.get_groups_uncomplete(user_id=user_id)
        return groups
