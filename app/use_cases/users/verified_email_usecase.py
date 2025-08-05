from ...repositories.user_repository import UserRepository
from ...services.token_service import TokenService
from ...constants.error_messages import ERROR_MESSAGES


class VerifiedEmailUseCase:
    def __init__(self, user_repo: UserRepository, token_service: TokenService):
        self.user_repo = user_repo
        self.token_service = token_service

    def execute(self, raw_token: str):
        # 1️⃣ Validate token input
        if not raw_token:
            raise ValueError(ERROR_MESSAGES["MISSING_VERIFICATION_TOKEN"])

        # 2️⃣ Verify token validity
        payload = self.token_service.verify_token(raw_token)
        if not payload:
            raise ValueError(ERROR_MESSAGES["INVALID_OR_EXPIRED_TOKEN"])

        # 3️⃣ Ensure token type is for email verification
        if payload.get("type") != "verify_email":
            raise ValueError(ERROR_MESSAGES["INVALID_TOKEN_TYPE"])

        email = payload.get("email")
        user_id = payload.get("user_id")
        if not email or not user_id:
            raise ValueError(ERROR_MESSAGES["MISSING_TOKEN_DATA"])

        # 4️⃣ Retrieve stored token
        stored_token = self.user_repo.get_verified_email_token(email)
        if not stored_token:
            raise ValueError(ERROR_MESSAGES["VERIFICATION_TOKEN_NOT_FOUND"])

        # 5️⃣ Match token hash
        if not self.token_service.match_token_hash(raw_token, stored_token.token_hash):
            raise ValueError(ERROR_MESSAGES["TOKEN_MISMATCH"])

        # 6️⃣ Confirm email
        self.user_repo.confirm_email(
            email_id=stored_token.email_id,
            token_id=stored_token.id
        )

        return {"message": ERROR_MESSAGES["EMAIL_VERIFIED_SUCCESS"]}
