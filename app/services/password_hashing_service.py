import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Tuple

import bcrypt


class PasswordHashingService:
    def __init__(self, pepper: Optional[str] = None):
        
        self.pepper = pepper.encode() if pepper else None
        
    def hash_password(self, password: str) -> str:
        # Convert password to bytes and add pepper if configured
        password_bytes = password.encode()
        if self.pepper:
            password_bytes += self.pepper
        
        # Generate salt and hash the password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        password_bytes = password.encode()
        if self.pepper:
            password_bytes += self.pepper
            
        hashed_bytes = hashed_password.encode()
        
        try:
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except ValueError:
            return False
