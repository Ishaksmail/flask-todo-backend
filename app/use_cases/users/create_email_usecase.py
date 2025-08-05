from datetime import datetime, timedelta, timezone

from ...domain.entities.email_entity import EmailEntity
from ...domain.entities.verified_email_token_entity import VerifiedEmailTokenEntity
from ...interfaces.user_repository_interface import IUserRepository
from ...services.mail_service import MailService
from ...services.token_service import TokenService
from ...constants.error_messages import ERROR_MESSAGES


class CreateVerifiedEmailTokenUseCase:
    def __init__(self,
                 user_repo: IUserRepository,
                 token_service: TokenService,
                 mail_service: MailService,
                 base_url: str):
        self.user_repo = user_repo
        self.token_service = token_service
        self.mail_service = mail_service
        self.base_url = base_url

    def execute(self, email_address: str, user_id: int):
        # 1️⃣ التحقق من صحة البيانات المدخلة
        if not email_address:
            raise ValueError(ERROR_MESSAGES["MISSING_EMAIL_ADDRESS"])
        if not user_id:
            raise ValueError(ERROR_MESSAGES["MISSING_USER_ID"])

        # 2️⃣ إنشاء الإيميل في قاعدة البيانات
        email_entity = EmailEntity(
            email_address=email_address,
            user_id=user_id,
            is_primary=False
        )
        new_email = self.user_repo.create_email(email_entity)

        # 3️⃣ إنشاء التوكن للتحقق
        try:
            raw_token, token_hash, expires = self.token_service.generate_token(
                email=email_address,
                user_id=user_id,
                token_type="verify_email",
                expires_delta=timedelta(hours=2)
            )
        except Exception:
            raise ValueError(ERROR_MESSAGES["TOKEN_GENERATION_FAILED"])

        # 4️⃣ تخزين التوكن في قاعدة البيانات
        token_entity = VerifiedEmailTokenEntity(
            token_hash=token_hash,
            is_used=False,
            expires_at=expires,
            created_at=datetime.now(timezone.utc),
            email_id=new_email.id
        )
        self.user_repo.create_verified_email_token(token_entity)

        # 5️⃣ إنشاء رابط التحقق
        verification_link = f"{self.base_url}/verify-email?token={raw_token}"

        # 6️⃣ إرسال البريد الإلكتروني للمستخدم
        email_sent = self.mail_service.send_email(
            subject="Verify Your Email Address",
            receivers=[email_address],
            message=(
                f"Hello,\n\n"
                f"Please verify your email address by clicking the link below:\n"
                f"{verification_link}\n\n"
                f"This link will expire in 2 hours.\n"
                f"If you did not request this, please ignore this email."
            )
        )

        if not email_sent:
            raise ValueError(ERROR_MESSAGES["EMAIL_SEND_FAILED"])

        # 7️⃣ إعادة الاستجابة
        return {
            "message": ERROR_MESSAGES["VERIFICATION_LINK_SENT"],
            "verification_token": raw_token  # يمكن حذفه في الإنتاج
        }
