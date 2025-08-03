# domain/entities/verified_email_token_entity.py
from datetime import datetime
from typing import Optional


class VerifiedEmailTokenEntity:
    def __init__(self, 
                 id: Optional[int],
                 token_hash: str,
                 is_used: bool = False,
                 expires_at: Optional[datetime] = None,
                 created_at: Optional[datetime] = None,
                 used_at: Optional[datetime] = None,
                 email_id: Optional[int] = None,
                 user_id: Optional[int] = None):
        self.id = id
        self.token_hash = token_hash
        self.is_used = is_used
        self.expires_at = expires_at
        self.created_at = created_at or datetime.now(timezone.utc)
        self.used_at = used_at
        self.email_id = email_id
        self.user_id = user_id
