from datetime import datetime, timezone

from ...repositories.user_repository import UserRepository
from ...services.password_hashing_service import PasswordHashingService
from ...services.token_service import TokenService
from ...constants.error_messages import ERROR_MESSAGES


class ResetPasswordUseCase:
    def __init__(self,
                 user_repo: UserRepository,
                 token_service: TokenService,
                 hashing_service: PasswordHashingService):
        self.user_repo = user_repo
        self.token_service = token_service
        self.hashing_service = hashing_service

    def execute(self, raw_token: str, new_password: str):
        # 1️⃣ Validate inputs
        if not raw_token:
            raise ValueError(ERROR_MESSAGES["MISSING_RESET_TOKEN"])
        if not new_password or len(new_password) < 8:
            raise ValueError(ERROR_MESSAGES["INVALID_NEW_PASSWORD"])

        # 2️⃣ Verify token
        payload = self.token_service.verify_token(raw_token)
        if not payload:
            raise ValueError(ERROR_MESSAGES["INVALID_OR_EXPIRED_TOKEN"])

        # 3️⃣ Check token type
        if payload.get("type") != "reset_password":
            raise ValueError(ERROR_MESSAGES["INVALID_TOKEN_TYPE"])

        token_hash = self.token_service._hash_token(raw_token)
        stored_token = self.user_repo.get_password_reset_token(token_hash)

        if not stored_token:
            raise ValueError(ERROR_MESSAGES["TOKEN_NOT_FOUND"])

        if stored_token.is_used:
            raise ValueError(ERROR_MESSAGES["TOKEN_ALREADY_USED"])

        # 4️⃣ Update password
        hashed_password = self.hashing_service.hash_password(new_password)
        user = self.user_repo.update_password(
            id=stored_token.user_id,
            new_password_hashing=hashed_password
        )
        if not user:
            raise ValueError(ERROR_MESSAGES["USER_NOT_FOUND"])

        # 5️⃣ Confirm token usage
        confirmed_token = self.user_repo.confirm_password_reset_token(
            token_id=stored_token.id
        )
        if not confirmed_token:
            raise ValueError(ERROR_MESSAGES["TOKEN_CONFIRMATION_FAILED"])

        return True
