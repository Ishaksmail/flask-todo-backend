from ...repositories.user_repository import UserRepository
from ...services.password_hashing_service import PasswordHashingService
from ...services.token_service import TokenService
from ...constants.error_messages import ERROR_MESSAGES


class LoginUseCase:
    def __init__(self,
                 user_repo: UserRepository,
                 hashing_service: PasswordHashingService,
                 token_service: TokenService):
        self.user_repo = user_repo
        self.hashing_service = hashing_service
        self.token_service = token_service

    def execute(self, username: str, password: str):
    
        if not username or not password:
            raise ValueError(ERROR_MESSAGES["USERNAME_AND_PASSWORD_REQUIRED"])
        
      

        # 2️⃣ جلب المستخدم من قاعدة البيانات
        user = self.user_repo.get_user(username = username)
        
      
        print(user)
        
        if not user:
            raise ValueError(ERROR_MESSAGES["INVALID_CREDENTIALS"])
        
      

        # 3️⃣ التحقق من كلمة المرور
        if not self.hashing_service.verify_password(password, user.password):
            raise ValueError(ERROR_MESSAGES["INVALID_CREDENTIALS"])

        # 4️⃣ التحقق من وجود بريد إلكتروني رئيسي ومؤكد
        primary_email = next((email for email in user.emails if email.is_primary and not email.is_deleted), None)
        if not primary_email:
            raise ValueError(ERROR_MESSAGES["NO_ACTIVE_PRIMARY_EMAIL"])

      

        if not primary_email.verified_at:
            raise ValueError(ERROR_MESSAGES["EMAIL_NOT_VERIFIED"])
        
        print('----------------------------------------------')
        

        return user
