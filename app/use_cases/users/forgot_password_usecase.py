from datetime import datetime, timedelta, timezone

from app.domain.entities.password_reset_token_entity import \
    PasswordResetTokenEntity
from app.interfaces.user_repository_interface import IUserRepository
from app.services.mail_service import MailService
from app.services.token_service import TokenService


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
       
        if not email:
            raise ValueError("البريد الإلكتروني مطلوب")

       
        db_email = self.user_repo.get_verified_email(email_address=email)

        if not db_email:
            raise ValueError("لا يوجد بريد إلكتروني مؤكد مرتبط بهذا الحساب")
        
        user_id = db_email.user_id
        raw_token, token_hash, expires = self.token_service.generate_token(
            email=email,
            user_id=user_id,
            token_type="reset_password",
            expires_delta=timedelta(hours=1)
        )

      
        token_entity = PasswordResetTokenEntity(
            token_hash=token_hash,
            is_used=False,
            expires_at=expires,
            created_at=datetime.now(timezone.utc),
            user_id=user_id
        )

        self.user_repo.create_password_reset_token(token_entity)

      
        reset_link = f"{self.base_url}/reset-password?token={raw_token}"

     
        self.mail_service.send_email(
            subject="إعادة تعيين كلمة المرور",
            receivers=[email],
            message=(
                f"مرحباً،\n\n"
                f"لقد طلبت إعادة تعيين كلمة المرور الخاصة بحسابك.\n"
                f"يمكنك تعيين كلمة مرور جديدة عبر الرابط التالي:\n{reset_link}\n\n"
                f"هذا الرابط صالح لمدة ساعة واحدة فقط."
            )
        )

        # 7️⃣ إعادة الاستجابة
        return {
            "message": "تم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني",
            "reset_token": raw_token
        }
