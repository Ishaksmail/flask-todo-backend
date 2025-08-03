from datetime import datetime, timezone

from app.repositories.user_repository import UserRepository
from app.services.password_hashing_service import PasswordHashingService
from app.services.token_service import TokenService


class ResetPasswordUseCase:
    def __init__(self,
                 user_repo: UserRepository,
                 token_service: TokenService,
                 hashing_service: PasswordHashingService):
        self.user_repo = user_repo
        self.token_service = token_service
        self.hashing_service = hashing_service

    def execute(self, raw_token: str, new_password: str):
        # 1️⃣ التحقق من الإدخالات
        if not raw_token:
            raise ValueError("رمز إعادة التعيين مفقود")
        if not new_password or len(new_password) < 6:
            raise ValueError("كلمة المرور الجديدة غير صالحة، يجب أن تكون 6 أحرف على الأقل")

        # 2️⃣ التحقق من صحة التوكن (JWT)
        payload = self.token_service.verify_token(raw_token)
        if not payload:
            raise ValueError("رمز إعادة تعيين كلمة المرور غير صالح أو منتهي الصلاحية")

        # 3️⃣ التحقق من أن التوكن مخصص لإعادة تعيين كلمة المرور
        if payload.get("type") != "reset_password":
            raise ValueError("نوع التوكن غير صالح لهذه العملية")

        token_hash = self.token_service._hash_token(raw_token)
        stored_token = self.user_repo.get_password_reset_token(token_hash)

        if not stored_token:
            raise ValueError("لم يتم العثور على رمز صالح لإعادة تعيين كلمة المرور")

        if stored_token.is_used:
            raise ValueError("تم استخدام هذا الرمز بالفعل")

        # 4️⃣ تحديث كلمة المرور
        hashed_password = self.hashing_service.hash_password(new_password)
        
        user = self.user_repo.update_password(id=stored_token.user_id,new_password_hashing=hashed_password)
        
        if not user:
            raise ValueError("المستخدم غير موجود")

        # 5️⃣ تأكيد استخدام التوكن
        confirmed_token = self.user_repo.confirm_password_reset_token(token_id=stored_token.id)

        if not confirmed_token:
            raise ValueError("لم يتم العثور على الرمز أو تم استخدامه بالفعل")

        return True
