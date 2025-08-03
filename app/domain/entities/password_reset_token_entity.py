# domain/entities/password_reset_token_entity.py
from datetime import datetime
from typing import Optional

class PasswordResetTokenEntity:
    def __init__(self,
                 id: Optional[int],
                 token_hash: str,
                 is_used: bool = False,
                 expires_at: Optional[datetime] = None,
                 used_at: Optional[datetime] = None,
                 created_at: Optional[datetime] = None,
                 user_id: Optional[int] = None):
        self.id = id
        self.token_hash = token_hash
        self.is_used = is_used
        self.expires_at = expires_at
        self.used_at = used_at
        self.created_at = created_at or datetime.now(timezone.utc)
        self.user_id = user_id
