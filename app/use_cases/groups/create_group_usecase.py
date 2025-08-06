from datetime import datetime, timezone
from ...interfaces.group_repository_interface import IGroupRepository
from ...domain.entities.group_entity import GroupEntity


class CreateGroupUseCase:
    def __init__(self, group_repository: IGroupRepository):
        self.group_repository = group_repository

    def execute(self, name: str, description: str, user_id: int):
    
        new_group = GroupEntity(
            id=None,
            name=name,
            description=description,
            is_deleted=False,
            deleted_at=None,
            created_at=datetime.now(timezone.utc),
            updated_at=None,
            user_id=user_id,
            tasks=[]
        )

        return self.group_repository.create_group(new_group)
