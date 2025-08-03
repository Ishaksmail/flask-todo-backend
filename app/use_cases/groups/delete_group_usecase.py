from ...interfaces.group_repository_interface import IGroupRepository


class DeleteGroupUseCase:
    def __init__(self, group_repo: IGroupRepository):
        self.group_repo = group_repo

    def execute(self, group_id: int) -> bool:
        """
        حذف مجموعة معينة (Soft Delete).
        :param group_id: معرف المجموعة
        :return: True إذا تم الحذف، False إذا لم يتم العثور على المجموعة
        """
        return self.group_repo.delete_group(group_id)
