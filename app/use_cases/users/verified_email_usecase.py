from app.repositories.user_repository import UserRepository
from app.services.token_service import TokenService


class VerifiedEmailUseCase:
    def __init__(self, user_repo: UserRepository, token_service: TokenService):
        self.user_repo = user_repo
        self.token_service = token_service

    def execute(self, raw_token: str):
        
        if not raw_token:
            raise ValueError("رمز التأكيد مفقود")

        
        payload = self.token_service.verify_token(raw_token)
        if not payload:
            raise ValueError("رمز التأكيد غير صالح أو منتهي الصلاحية")

        if payload.get("type") != "verify_email":
            raise ValueError("نوع التوكن غير صالح لهذه العملية")

        email = payload.get("email")
        user_id = payload.get("user_id")
        if not email or not user_id:
            raise ValueError("بيانات التوكن غير كاملة")

        
        stored_token = self.user_repo.get_verified_email_token(email)
        if not stored_token:
            raise ValueError("لم يتم العثور على رمز صالح لهذا البريد الإلكتروني")

        
        if not self.token_service.match_token_hash(raw_token, stored_token.token_hash):
            raise ValueError("رمز التأكيد لا يطابق السجل المخزن")

        
        self.user_repo.confirm_email(
            email_id=stored_token.email_id,
            token_id=stored_token.id
        )

        return {"message": "تم تأكيد البريد الإلكتروني بنجاح"}
