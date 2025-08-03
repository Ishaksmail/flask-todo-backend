# domain/entities/email_entity.py
from datetime import datetime
from typing import Optional

class EmailEntity:
    def __init__(self, 
                 id: Optional[int], 
                 email_address: str, 
                 is_primary: bool = False, 
                 is_deleted: bool = False,
                 deleted_at: Optional[datetime] = None,
                 verified_at: Optional[datetime] = None,
                 user_id: Optional[int] = None):
        self.id = id
        self.email_address = email_address
        self.is_primary = is_primary
        self.is_deleted = is_deleted
        self.deleted_at = deleted_at
        self.verified_at = verified_at
        self.user_id = user_id
