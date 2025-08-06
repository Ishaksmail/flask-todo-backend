from ...interfaces.group_repository_interface import IGroupRepository


class DeleteGroupUseCase:
    def __init__(self, group_repository: IGroupRepository):
        self.group_repository = group_repository

    def execute(self, group_id: int, user_id:int) -> bool:
        return self.group_repository.delete_group(group_id,user_id)
