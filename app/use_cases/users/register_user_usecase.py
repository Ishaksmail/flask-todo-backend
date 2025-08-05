from datetime import datetime, timedelta, timezone

from ...domain.entities.email_entity import EmailEntity
from ...domain.entities.user_entity import UserEntity
from ...domain.entities.verified_email_token_entity import VerifiedEmailTokenEntity
from ...repositories.user_repository import UserRepository
from ...services.mail_service import MailService
from ...services.password_hashing_service import PasswordHashingService
from ...services.token_service import TokenService
from ...constants.error_messages import ERROR_MESSAGES


class RegisterUserUseCase:
    def __init__(self,
                 user_repo: UserRepository,
                 hashing_service: PasswordHashingService,
                 token_service: TokenService,
                 mail_service: MailService,
                 base_url: str):
        self.user_repo = user_repo
        self.hashing_service = hashing_service
        self.token_service = token_service
        self.mail_service = mail_service
        self.base_url = base_url

    def execute(self, username: str, email: str, password: str):
        # 1️⃣ Validate inputs
        if not username or not email or not password:
            raise ValueError(ERROR_MESSAGES["ALL_FIELDS_REQUIRED"])

        # 2️⃣ Hash password
        hashed_password = self.hashing_service.hash_password(password)

        # 3️⃣ Create new user entity
        new_user = UserEntity(
            username=username,
            password=hashed_password,
            created_at=datetime.now(timezone.utc),
            emails=[
                EmailEntity(
                    email_address=email,
                    is_primary=True,
                    user_id=None  # Will be filled after user creation
                )
            ]
        )

        # 4️⃣ Save user
        created_user = self.user_repo.create_user(new_user)

        # 5️⃣ Generate email verification token
        raw_token, token_hash, expires = self.token_service.generate_token(
            email=email,
            user_id=created_user.id,
            token_type="verify_email",
            expires_delta=timedelta(hours=24)
        )

        # 6️⃣ Store token
        token_entity = VerifiedEmailTokenEntity(
            token_hash=token_hash,
            is_used=False,
            expires_at=expires,
            created_at=datetime.now(timezone.utc),
            email_id=created_user.emails[0].id,
            user_id=created_user.id
        )
        self.user_repo.create_verified_email_token(token_entity)

        # 7️⃣ Send verification email
        verification_link = f"{self.base_url}/verify-email?token={raw_token}"
        self.mail_service.send_email(
            subject="Verify Your Email",
            receivers=[email],
            message=(
                f"Hello {username},\n\n"
                f"Please verify your email by clicking the following link:\n"
                f"{verification_link}\n\n"
                f"This link is valid for 24 hours."
            )
        )

        return created_user
