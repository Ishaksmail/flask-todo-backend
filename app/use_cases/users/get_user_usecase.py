from ...repositories.user_repository import UserRepository

class GetUserUseCase:
    def __init__(self,
                 user_repo: UserRepository):
        self.user_repo = user_repo
        
    def execute(self, username: str):
        if not username:
            raise ValueError(ERROR_MESSAGES["USERNAME_REQUIRED"])
        
        return self.user_repo.get_user(username=username)
