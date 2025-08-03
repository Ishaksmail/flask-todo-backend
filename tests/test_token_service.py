import pytest
from datetime import timedelta, datetime
from app.services.token_service import TokenService

@pytest.fixture
def token_service():
    return TokenService(secret_key="test_secret", algorithm="HS256", token_expire_minutes=30)

def test_generate_and_verify_token_success(token_service):
    raw_token, token_hash, expires = token_service.generate_token(
        email="user@example.com",
        user_id=1,
        token_type="email_verification"
    )

    payload = token_service.verify_token(raw_token)
    
    assert payload is not None
    assert payload["email"] == "user@example.com"
    assert payload["user_id"] == 1
    assert payload["type"] == "email_verification"
    assert isinstance(expires, datetime)
    assert token_service.match_token_hash(raw_token, token_hash) is True

def test_verify_token_expired(token_service):
    raw_token, _, _ = token_service.generate_token(
        email="user@example.com",
        user_id=1,
        token_type="password_reset",
        expires_delta=timedelta(seconds=-1)  # انتهت مدة الصلاحية
    )
    payload = token_service.verify_token(raw_token)
    assert payload is None

def test_match_token_hash_failure(token_service):
    raw_token, token_hash, _ = token_service.generate_token(
        email="user@example.com",
        user_id=1,
        token_type="email_verification"
    )
    assert token_service.match_token_hash(raw_token, "wrong_hash") is False
