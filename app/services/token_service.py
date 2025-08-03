import hashlib
from datetime import datetime, timedelta ,timezone
from typing import Optional, Tuple

import jwt
from jwt import PyJWTError


class TokenService:
    def __init__(self, secret_key: str, algorithm: str = "HS256", token_expire_minutes: int = 30):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expire_minutes = token_expire_minutes

    def _hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def generate_token(self, email: str, user_id: int,token_type: str, expires_delta: Optional[timedelta] = None) -> Tuple[str, str, datetime]:
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=self.token_expire_minutes))
        payload = {
            "email": email,
            "user_id": user_id,
            "type": token_type,
            "exp": expire
        }
        raw_token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        token_hash = self._hash_token(raw_token)

        return raw_token, token_hash, expire

    def verify_token(self, raw_token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(raw_token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except PyJWTError:
            return None

    def match_token_hash(self, raw_token: str, stored_hash: str) -> bool:
        return self._hash_token(raw_token) == stored_hash
