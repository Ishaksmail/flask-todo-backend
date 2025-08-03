from datetime import datetime,timezone
from typing import Optional, List
from .email_entity import EmailEntity

class UserEntity:
    def __init__(self, 
                 username: str, 
                 password: str, 
                 id: Optional[int] = None, 
                 created_at: Optional[datetime] = None,
                 emails: Optional[List['EmailEntity']] = None):
        self.id = id
        self.username = username
        self.password = password
        self.created_at = created_at or datetime.now(timezone.utc)
        self.emails = emails or []
