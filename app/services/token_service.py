import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

import jwt
from jwt import PyJWTError
from ..constants.error_messages import ERROR_MESSAGES


class TokenService:
    def __init__(self, secret_key: str, algorithm: str = "HS256", token_expire_minutes: int = 30):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expire_minutes = token_expire_minutes

    def _hash_token(self, token: str) -> str:
        if not token:
            raise ValueError(ERROR_MESSAGES["TOKEN_NOT_FOUND"])
        return hashlib.sha256(token.encode()).hexdigest()

    def generate_token(self, email: str, user_id: int, token_type: str,
                       expires_delta: Optional[timedelta] = None) -> Tuple[str, str, datetime]:
        if not email or not user_id or not token_type:
            raise ValueError(ERROR_MESSAGES["TOKEN_GENERATION_FAILED"])

        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=self.token_expire_minutes))
        payload = {
            "email": email,
            "user_id": user_id,
            "type": token_type,
            "exp": expire
        }

        try:
            raw_token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            token_hash = self._hash_token(raw_token)
        except Exception:
            raise ValueError(ERROR_MESSAGES["TOKEN_GENERATION_FAILED"])

        return raw_token, token_hash, expire

    def verify_token(self, raw_token: str) -> Optional[dict]:
        if not raw_token:
            raise ValueError(ERROR_MESSAGES["TOKEN_NOT_FOUND"])
        try:
            payload = jwt.decode(raw_token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except PyJWTError:
            raise ValueError(ERROR_MESSAGES["TOKEN_INVALID_OR_EXPIRED"])

    def match_token_hash(self, raw_token: str, stored_hash: str) -> bool:
        if not raw_token or not stored_hash:
            raise ValueError(ERROR_MESSAGES["TOKEN_MATCH_FAILED"])
        return self._hash_token(raw_token) == stored_hash
