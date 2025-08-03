from typing import List, Optional, Protocol, Tuple

from app.domain.entities.email_entity import EmailEntity
from app.domain.entities.password_reset_token_entity import \
    PasswordResetTokenEntity
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.verified_email_token_entity import \
    VerifiedEmailTokenEntity


class IUserRepository(Protocol):
    
    def get_user(self, username: str) -> Optional[UserEntity]:
        ...
    
    def create_user(self, user_entity:UserEntity) -> UserEntity:
        ...

    def update_user(self, user_entity:UserEntity) -> UserEntity:
        ...
        
    def create_email(self, email_entity: EmailEntity) -> EmailEntity:
        ...
    
    def delete_email(self, email_id: int) -> bool:
        ...
    
    def create_verified_email_token(self, verified_email_token: VerifiedEmailTokenEntity) -> VerifiedEmailTokenEntity:
        ...
    
    def get_verified_email_token(self, email_address: str) -> Optional[VerifiedEmailTokenEntity]:
        ...
    
    def create_password_reset_token(self, password_reset_token: PasswordResetTokenEntity) -> PasswordResetTokenEntity:
        ...
    
    def get_password_reset_token(self, token_hash: str) -> Optional[PasswordResetTokenEntity]:
        ...
        
    # helper
    
    def _convert_user_to_entity(self, db_user: User) -> UserEntity:
        ...
    
    def _convert_email_to_entity(self, db_email: Email) -> EmailEntity: 
        ...
    
    def _convert_verified_token_to_entity(self, db_token: VerifiedEmailToken) -> VerifiedEmailTokenEntity:
        ...
    
    def _convert_password_token_to_entity(self, db_token: PasswordResetToken) -> PasswordResetTokenEntity:
        ...
    
    
    
    