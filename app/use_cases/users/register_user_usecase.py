from datetime import datetime, timedelta,timezone

from app.domain.entities.email_entity import EmailEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.verified_email_token_entity import \
    VerifiedEmailTokenEntity
from app.repositories.user_repository import UserRepository
from app.services.mail_service import MailService
from app.services.password_hashing_service import PasswordHashingService
from app.services.token_service import TokenService


class RegisterUserUseCase:
    def __init__(self,
                 user_repo: UserRepository,
                 hashing_service: PasswordHashingService,
                 token_service: TokenService,
                 mail_service: MailService,
                base_url:str):
        self.user_repo = user_repo
        self.hashing_service = hashing_service
        self.token_service = token_service
        self.mail_service = mail_service
        self.base_url = base_url

    def execute(self, username: str, email: str, password: str):
        # 1️⃣ التحقق من المدخلات
        if not username or not email or not password:
            raise ValueError("جميع الحقول مطلوبة")

        # 2️⃣ تشفير كلمة المرور
        hashed_password = self.hashing_service.hash_password(password)

        # 3️⃣ إنشاء المستخدم الجديد
        new_user = UserEntity(
            username=username,
            password=hashed_password,
            created_at=datetime.now(timezone.utc),
            emails=[
                EmailEntity(
                    email_address=email,
                    is_primary=True,
                    user_id=None  # يملأ بعد إنشاء المستخدم
                )
            ]
        )

        # 4️⃣ حفظ المستخدم
        created_user = self.user_repo.create_user(new_user)

        # 5️⃣ إنشاء توكن لتأكيد البريد الإلكتروني
        raw_token, token_hash, expires = self.token_service.generate_token(
            email=email,
            user_id=created_user.id,
            token_type="verify_email",
            expires_delta=timedelta(hours=24)
        )

        # 6️⃣ تخزين التوكن في قاعدة البيانات
        token_entity = VerifiedEmailTokenEntity(
            token_hash=token_hash,
            is_used=False,
            expires_at=expires,
            created_at=datetime.now(timezone.utc),
            email_id=created_user.emails[0].id,
            user_id=created_user.id
        )
        self.user_repo.create_verified_email_token(token_entity)

        # 7️⃣ إرسال رسالة تأكيد
        verification_link = f"{self.base_url}/verify-email?token={raw_token}"
        self.mail_service.send_email(
            subject="تأكيد البريد الإلكتروني",
            receivers=[email],
            message=f"مرحباً {username},\n\nيرجى تأكيد بريدك الإلكتروني عبر الرابط التالي:\n{verification_link}\n\nهذا الرابط صالح لمدة 24 ساعة."
        )

        return {
            "message": "تم إنشاء الحساب بنجاح. تحقق من بريدك الإلكتروني لتأكيد الحساب.",
            "user_id": created_user.id
        }
