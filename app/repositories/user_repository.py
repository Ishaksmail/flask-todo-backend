from datetime import datetime

from sqlalchemy.orm import Session

from ..domain.entities.email_entity import EmailEntity
from ..domain.entities.password_reset_token_entity import \
    PasswordResetTokenEntity
from ..domain.entities.user_entity import UserEntity
from ..domain.entities.verified_email_token_entity import \
    VerifiedEmailTokenEntity
from ..infrastructure.database.models import (Email, PasswordResetToken, User,
                                              VerifiedEmailToken)
from ..interfaces.user_repository_interface import IUserRepository
from ._decorator import handle_db_errors


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session
        
    def _convert_user_to_entity(self, db_user: User):
        
        db_emails = self.session.query(Email).filter(
            Email.user_id == db_user.id,
            Email.is_deleted == False
        ).all()
        
        emails = [self._convert_email_to_entity(email) for email in db_emails]
        
        user_entity = UserEntity(
            id=db_user.id,
            username=db_user.username,
            password=db_user.password,
            created_at=db_user.created_at,
            emails=emails
        )
        
        return user_entity
    
    def _convert_email_to_entity(self, db_email: Email) -> EmailEntity:
        return EmailEntity(
            id=db_email.id,
            email_address=db_email.email_address,
            is_primary=db_email.is_primary,
            is_deleted=db_email.is_deleted,
            deleted_at=db_email.deleted_at,
            verified_at=db_email.verified_at,
            user_id=db_email.user_id
        )
    
    def _convert_verified_token_to_entity(self, db_token: VerifiedEmailToken) -> VerifiedEmailTokenEntity:
        return VerifiedEmailTokenEntity(
            id=db_token.id,
            token_hash=db_token.token_hash,
            is_used=db_token.is_used,
            expires_at=db_token.expires_at,
            created_at=db_token.created_at,
            used_at=db_token.used_at,
            email_id=db_token.email_id,
            user_id=db_token.user_id
        )
    
    def _convert_password_token_to_entity(self, db_token: PasswordResetToken) -> PasswordResetTokenEntity:
        return PasswordResetTokenEntity(
            id=db_token.id,
            token_hash=db_token.token_hash,
            is_used=db_token.is_used,
            expires_at=db_token.expires_at,
            created_at=db_token.created_at,
            used_at=db_token.used_at,
            user_id=db_token.user_id
        )
    
    def get_user(self, username: str):
        db_user = self.session.query(User).filter(User.username == username).first()
        if not db_user:
            return None
        
        return self._convert_user_to_entity(db_user)
    
    def create_user(self, user_entity: UserEntity):
        existing_user = self.session.query(User).filter(
            User.username == user_entity.username
        ).first()
        
        if existing_user:
            raise ValueError("اسم المستخدم موجود مسبقاً")

        # 3. إنشاء المستخدم
        db_user = User(
            username=user_entity.username,
            password=user_entity.password,
            created_at=user_entity.created_at or datetime.utcnow()
        )
        
        self.session.add(db_user)
        self.session.flush() 

        # 4. معالجة عناوين البريد الإلكتروني
        for email_entity in user_entity.emails:
            # التحقق من عدم تكرار البريد الإلكتروني
            existing_email = self.session.query(Email).filter(
                Email.email_address == email_entity.email_address,
                Email.is_deleted == False
            ).first()
            
            if existing_email:
                self.session.rollback()
                raise ValueError(f"البريد الإلكتروني {email_entity.email_address} موجود مسبقاً")
            
            # إنشاء سجل البريد الإلكتروني
            db_email = Email(
                email_address=email_entity.email_address,
                is_primary=email_entity.is_primary,
                user_id=db_user.id,
                verified_at=datetime.utcnow()
            )
            
            self.session.add(db_email)
            self.session.flush()
            email_entity.id = db_email.id

        primary_count = sum(1 for e in user_entity.emails if e.is_primary)
        if primary_count != 1:
            self.session.rollback()
            raise ValueError("يجب أن يكون هناك بريد إلكتروني أساسي واحد بالضبط")

        self.session.commit()
        self.session.refresh(db_user)
        
        user_entity.id = db_user.id
        return user_entity
    
    def update_user(self, user_entity: UserEntity):
        db_user = self.session.query(User).filter(User.id == user_entity.id).first()
        if not db_user:
            return None
        
        db_user.username = user_entity.username
        db_user.password = user_entity.password
        
        self.session.commit()
        self.session.refresh(db_user)
        
        return UserEntity(
            id=db_user.id,
            username=db_user.username,
            password=db_user.password,
            created_at=db_user.created_at
        )
    
    def create_email(self, email_entity: EmailEntity):
        db_email = Email(
            email_address=email_entity.email_address,
            is_primary=email_entity.is_primary,
            user_id=email_entity.user_id
        )
        
        self.session.add(db_email)
        self.session.commit()
        self.session.refresh(db_email)
        
        email_entity.id = db_email.id
        return email_entity
    
    def delete_email(self, email_id: int):
        db_email = self.session.query(Email).filter(Email.id == email_id).first()
        if not db_email:
            return None
        
        db_email.is_deleted = True
        db_email.deleted_at = datetime.utcnow()
        
        self.session.commit()
        return self._convert_email_to_entity(db_email)
    
    def create_verified_email_token(self, token: VerifiedEmailTokenEntity):
        db_token = VerifiedEmailToken(
            token_hash=token.token_hash,
            expires_at=token.expires_at,
            email_id=token.email_id,
            user_id=token.user_id
        )
        
        self.session.add(db_token)
        self.session.commit()
        self.session.refresh(db_token)
        
        token.id = db_token.id
        token.created_at = db_token.created_at
        return token
    
    def get_verified_email_token(self, email_address: str):
        db_email = self.session.query(Email).filter(
            Email.email_address == email_address
        ).first()
        
        if not db_email:
            return None
            
        db_token = self.session.query(VerifiedEmailToken).filter(
            VerifiedEmailToken.email_id == db_email.id,
            VerifiedEmailToken.is_used == False,
            VerifiedEmailToken.expires_at > datetime.utcnow()
        ).order_by(VerifiedEmailToken.created_at.desc()).first()
        
        if not db_token:
            return None
            
        return self._convert_verified_token_to_entity(db_token)
    
    def create_password_reset_token(self, token: PasswordResetTokenEntity):
        db_token = PasswordResetToken(
            token_hash=token.token_hash,
            expires_at=token.expires_at,
            user_id=token.user_id
        )
        
        self.session.add(db_token)
        self.session.commit()
        self.session.refresh(db_token)
        
        token.id = db_token.id
        token.created_at = db_token.created_at
        return token
    
    def get_password_reset_token(self, token_hash: str) -> Optional[PasswordResetTokenEntity]:
        db_token = self.session.query(PasswordResetToken).filter(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.is_used == False,
            PasswordResetToken.expires_at > datetime.utcnow()
        ).first()
        
        if not db_token:
            return None
            
        return self._convert_password_token_to_entity(db_token)
    