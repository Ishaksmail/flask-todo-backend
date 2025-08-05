import pytest
import jwt
from datetime import datetime, timedelta, timezone
from app.services.token_service import TokenService
from app.constants.error_messages import ERROR_MESSAGES


SECRET_KEY = "test_secret_key"
ALGORITHM = "HS256"


@pytest.fixture
def token_service():
    return TokenService(secret_key=SECRET_KEY, algorithm=ALGORITHM, token_expire_minutes=1)


def test_generate_token_success(token_service):
    raw_token, token_hash, expire = token_service.generate_token(
        email="test@example.com",
        user_id=123,
        token_type="verify_email"
    )

    assert isinstance(raw_token, str)
    assert isinstance(token_hash, str)
    assert isinstance(expire, datetime)


def test_generate_token_missing_data_raises_error(token_service):
    with pytest.raises(ValueError) as exc:
        token_service.generate_token(email="", user_id=123, token_type="verify_email")
    assert str(exc.value) == ERROR_MESSAGES["TOKEN_GENERATION_FAILED"]


def test_hash_token_success(token_service):
    token = "sample_token"
    result = token_service._hash_token(token)
    assert isinstance(result, str)
    assert len(result) == 64  # SHA-256 hash length


def test_hash_token_missing_token_raises_error(token_service):
    with pytest.raises(ValueError) as exc:
        token_service._hash_token("")
    assert str(exc.value) == ERROR_MESSAGES["TOKEN_NOT_FOUND"]


def test_verify_token_success(token_service):
    raw_token, _, _ = token_service.generate_token(
        email="test@example.com",
        user_id=123,
        token_type="verify_email"
    )

    payload = token_service.verify_token(raw_token)
    assert payload["email"] == "test@example.com"
    assert payload["user_id"] == 123
    assert payload["type"] == "verify_email"


def test_verify_token_invalid_token_raises_error(token_service):
    with pytest.raises(ValueError) as exc:
        token_service.verify_token("invalid_token")
    assert str(exc.value) == ERROR_MESSAGES["TOKEN_INVALID_OR_EXPIRED"]


def test_verify_token_expired_token_raises_error(token_service):
    expired_payload = {
        "email": "test@example.com",
        "user_id": 123,
        "type": "verify_email",
        "exp": datetime.now(timezone.utc) - timedelta(seconds=1)
    }
    expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(ValueError) as exc:
        token_service.verify_token(expired_token)
    assert str(exc.value) == ERROR_MESSAGES["TOKEN_INVALID_OR_EXPIRED"]


def test_match_token_hash_success(token_service):
    raw_token = "sample_token"
    hashed = token_service._hash_token(raw_token)
    assert token_service.match_token_hash(raw_token, hashed) is True


def test_match_token_hash_mismatch(token_service):
    assert token_service.match_token_hash("token1", token_service._hash_token("token2")) is False


def test_match_token_hash_missing_data_raises_error(token_service):
    with pytest.raises(ValueError) as exc:
        token_service.match_token_hash("", "")
    assert str(exc.value) == ERROR_MESSAGES["TOKEN_MATCH_FAILED"]
