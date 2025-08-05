import bcrypt
from typing import Optional
from ..constants.error_messages import ERROR_MESSAGES

class PasswordHashingService:
    def __init__(self, pepper: Optional[str] = None):
        self.pepper = pepper.encode() if pepper else None

    def hash_password(self, password: str) -> str:
        if not password or len(password) < 8:
            raise ValueError(ERROR_MESSAGES["INVALID_PASSWORD_LENGTH"])

        password_bytes = password.encode()
        if self.pepper:
            password_bytes += self.pepper

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)

        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        if not password or not hashed_password:
            raise ValueError(ERROR_MESSAGES["INVALID_PASSWORD_INPUTS"])

        password_bytes = password.encode()
        if self.pepper:
            password_bytes += self.pepper

        hashed_bytes = hashed_password.encode()

        try:
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except ValueError:
            raise ValueError(ERROR_MESSAGES["PASSWORD_VERIFICATION_FAILED"])
