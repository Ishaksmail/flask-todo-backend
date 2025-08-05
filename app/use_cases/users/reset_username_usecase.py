from ...repositories.user_repository import UserRepository
from ...constants.error_messages import ERROR_MESSAGES


class ResetUsernameUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, old_username: str, new_username: str):
        # 1️⃣ Validate inputs
        if not old_username:
            raise ValueError(ERROR_MESSAGES["MISSING_CURRENT_USERNAME"])
        if not new_username or len(new_username) < 3:
            raise ValueError(ERROR_MESSAGES["INVALID_NEW_USERNAME"])

        # 2️⃣ Update username
        updated_user = self.user_repo.update_username(
            old_username=old_username,
            new_username=new_username
        )

        if not updated_user:
            raise ValueError(ERROR_MESSAGES["USERNAME_UPDATE_FAILED"])

        return updated_user
