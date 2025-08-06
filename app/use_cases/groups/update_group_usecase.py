from datetime import datetime, timezone
from ...interfaces.group_repository_interface import IGroupRepository
from ...domain.entities.group_entity import GroupEntity


class UpdateGroupUseCase:
    def __init__(self, group_repository: IGroupRepository):
        self.group_repository = group_repository

    def execute(self, group_id: int, name: str, description: str) -> GroupEntity | None:
        updated_group = GroupEntity(
            id=group_id,
            name=name,
            description=description,
            is_deleted=False,
            deleted_at=None,
            created_at=None,  # لا نغير تاريخ الإنشاء
            updated_at=datetime.now(timezone.utc),
            user_id=None,     # لن نغير المالك
            tasks=[]
        )

        return self.group_repository.update_group(updated_group)
