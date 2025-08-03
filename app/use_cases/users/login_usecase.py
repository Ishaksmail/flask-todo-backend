from datetime import datetime, timedelta

from app.repositories.user_repository import UserRepository
from app.services.password_hashing_service import PasswordHashingService
from app.services.token_service import TokenService


class LoginUseCase:
    def __init__(self,
                 user_repo: UserRepository,
                 hashing_service: PasswordHashingService,
                 token_service: TokenService):
        self.user_repo = user_repo
        self.hashing_service = hashing_service
        self.token_service = token_service

    def execute(self, username: str, password: str):
        # 1️⃣ التحقق من إدخال الحقول
        if not username or not password:
            raise ValueError("اسم المستخدم وكلمة المرور مطلوبان")

        # 2️⃣ جلب المستخدم من قاعدة البيانات
        user = self.user_repo.get_user(username)
        if not user:
            raise ValueError("اسم المستخدم أو كلمة المرور غير صحيحة")

        # 3️⃣ التحقق من كلمة المرور
        if not self.hashing_service.verify_password(password, user.password):
            raise ValueError("اسم المستخدم أو كلمة المرور غير صحيحة")

        # 4️⃣ التحقق من وجود بريد إلكتروني رئيسي ومؤكد
        primary_email = next((email for email in user.emails if email.is_primary and not email.is_deleted), None)
        if not primary_email:
            raise ValueError("لا يوجد بريد إلكتروني أساسي نشط لهذا الحساب")

        if not primary_email.verified_at:
            raise ValueError("يجب تأكيد البريد الإلكتروني قبل تسجيل الدخول")


        return user
