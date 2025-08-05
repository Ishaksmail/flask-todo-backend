import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

from app.use_cases.users.register_user_usecase import RegisterUserUseCase
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.email_entity import EmailEntity
from app.constants.error_messages import ERROR_MESSAGES


@pytest.fixture
def setup_dependencies():
    user_repo = MagicMock()
    hashing_service = MagicMock()
    token_service = MagicMock()
    mail_service = MagicMock()
    base_url = "http://localhost:8000"

    return user_repo, hashing_service, token_service, mail_service, base_url


def test_register_user_success(setup_dependencies):
    user_repo, hashing_service, token_service, mail_service, base_url = setup_dependencies

    # Mock data
    hashing_service.hash_password.return_value = "hashed_password_123"

    mock_user = UserEntity(
        id=1,
        username="john_doe",
        password="hashed_password_123",
        created_at=datetime.now(timezone.utc),
        emails=[EmailEntity(id=10, email_address="john@example.com", is_primary=True, user_id=1)]
    )
    user_repo.create_user.return_value = mock_user

    token_service.generate_token.return_value = ("raw_token_abc", "token_hash_abc", datetime.now(timezone.utc) + timedelta(hours=24))

    # Initialize use case
    usecase = RegisterUserUseCase(user_repo, hashing_service, token_service, mail_service, base_url)

    # Execute
    created_user = usecase.execute("john_doe", "john@example.com", "StrongPass123")

    # Assertions
    hashing_service.hash_password.assert_called_once_with("StrongPass123")
    user_repo.create_user.assert_called_once()
    token_service.generate_token.assert_called_once_with(
        email="john@example.com",
        user_id=1,
        token_type="verify_email",
        expires_delta=timedelta(hours=24)
    )
    user_repo.create_verified_email_token.assert_called_once()
    mail_service.send_email.assert_called_once()
    assert created_user.username == "john_doe"
    assert created_user.emails[0].email_address == "john@example.com"


def test_register_user_missing_fields(setup_dependencies):
    user_repo, hashing_service, token_service, mail_service, base_url = setup_dependencies
    usecase = RegisterUserUseCase(user_repo, hashing_service, token_service, mail_service, base_url)

    with pytest.raises(ValueError) as exc:
        usecase.execute("", "user@example.com", "pass1234")
    assert str(exc.value) == ERROR_MESSAGES["ALL_FIELDS_REQUIRED"]

    with pytest.raises(ValueError) as exc:
        usecase.execute("john_doe", "", "pass1234")
    assert str(exc.value) == ERROR_MESSAGES["ALL_FIELDS_REQUIRED"]

    with pytest.raises(ValueError) as exc:
        usecase.execute("john_doe", "user@example.com", "")
    assert str(exc.value) == ERROR_MESSAGES["ALL_FIELDS_REQUIRED"]


def test_register_user_sends_verification_email(setup_dependencies):
    user_repo, hashing_service, token_service, mail_service, base_url = setup_dependencies

    hashing_service.hash_password.return_value = "hashed_password_123"
    mock_user = UserEntity(
        id=5,
        username="alice",
        password="hashed_password_123",
        created_at=datetime.now(timezone.utc),
        emails=[EmailEntity(id=15, email_address="alice@example.com", is_primary=True, user_id=5)]
    )
    user_repo.create_user.return_value = mock_user
    token_service.generate_token.return_value = ("token_raw", "token_hash", datetime.now(timezone.utc) + timedelta(hours=24))

    usecase = RegisterUserUseCase(user_repo, hashing_service, token_service, mail_service, base_url)

    usecase.execute("alice", "alice@example.com", "SecretPass123")

    mail_service.send_email.assert_called_once()
    args, kwargs = mail_service.send_email.call_args
    assert "Verify Your Email" in kwargs["subject"]
    assert "alice" in kwargs["message"]
    assert "token_raw" in kwargs["message"]
