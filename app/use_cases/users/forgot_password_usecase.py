from datetime import datetime, timedelta, timezone

from ...domain.entities.password_reset_token_entity import PasswordResetTokenEntity
from ...interfaces.user_repository_interface import IUserRepository
from ...services.mail_service import MailService
from ...services.token_service import TokenService
from ...constants.error_messages import ERROR_MESSAGES


class ForgotPasswordUseCase:
    def __init__(self,
                 user_repo: IUserRepository,
                 token_service: TokenService,
                 mail_service: MailService,
                 base_url: str):
        self.user_repo = user_repo
        self.token_service = token_service
        self.mail_service = mail_service
        self.base_url = base_url

    def execute(self, email: str):
        # 1️⃣ التحقق من الإدخال
        if not email:
            raise ValueError(ERROR_MESSAGES["EMAIL_REQUIRED"])

        # 2️⃣ التحقق من وجود البريد الإلكتروني المؤكد
        db_email = self.user_repo.get_verified_email(email_address=email)
        if not db_email:
            raise ValueError(ERROR_MESSAGES["EMAIL_NOT_VERIFIED"])

        user_id = db_email.user_id

        # 3️⃣ إنشاء التوكن
        try:
            raw_token, token_hash, expires = self.token_service.generate_token(
                email=email,
                user_id=user_id,
                token_type="reset_password",
                expires_delta=timedelta(hours=1)
            )
        except Exception:
            raise ValueError(ERROR_MESSAGES["TOKEN_GENERATION_FAILED"])

        # 4️⃣ حفظ التوكن في قاعدة البيانات
        token_entity = PasswordResetTokenEntity(
            token_hash=token_hash,
            is_used=False,
            expires_at=expires,
            created_at=datetime.now(timezone.utc),
            user_id=user_id
        )
        self.user_repo.create_password_reset_token(token_entity)

        # 5️⃣ إنشاء الرابط
        reset_link = f"{self.base_url}/reset-password?token={raw_token}"

        # 6️⃣ إرسال البريد الإلكتروني
        email_sent = self.mail_service.send_email(
            subject="Password Reset Request",
            receivers=[email],
            message=(
                f"Hello,\n\n"
                f"You requested to reset your password.\n"
                f"Please click the link below to set a new password:\n{reset_link}\n\n"
                f"This link is valid for one hour only."
            )
        )

        if not email_sent:
            raise ValueError(ERROR_MESSAGES["EMAIL_SEND_FAILED"])

        # 7️⃣ إعادة الاستجابة
        return {
            "message": ERROR_MESSAGES["PASSWORD_RESET_LINK_SENT"],
            "reset_token": raw_token
        }
