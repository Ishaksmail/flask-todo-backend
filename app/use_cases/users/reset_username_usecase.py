from app.repositories.user_repository import UserRepository


class ResetUsernameUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, old_username: str, new_username: str):
        if not old_username:
            raise ValueError("اسم المستخدم الحالي مفقود")
        if not new_username or len(new_username) < 3:
            raise ValueError("اسم المستخدم الجديد غير صالح، يجب أن يكون 3 أحرف على الأقل")

        updated_user = self.user_repo.update_username(
            old_username=old_username,
            new_username=new_username
        )

        if not updated_user:
            raise ValueError("المستخدم غير موجود أو فشل التحديث")

        return updated_user
