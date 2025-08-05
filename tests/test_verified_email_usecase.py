import pytest
from unittest.mock import MagicMock
from app.use_cases.users.verified_email_usecase import VerifiedEmailUseCase
from app.constants.error_messages import ERROR_MESSAGES


class MockToken:
    def __init__(self, id=1, email_id=10, token_hash="hashed_token"):
        self.id = id
        self.email_id = email_id
        self.token_hash = token_hash


@pytest.fixture
def setup_dependencies():
    user_repo = MagicMock()
    token_service = MagicMock()
    return user_repo, token_service


def test_execute_success(setup_dependencies):
    user_repo, token_service = setup_dependencies

    raw_token = "valid_token"
    payload = {
        "email": "test@example.com",
        "user_id": 1,
        "type": "verify_email"
    }

    stored_token = MockToken()

    token_service.verify_token.return_value = payload
    user_repo.get_verified_email_token.return_value = stored_token
    token_service.match_token_hash.return_value = True

    usecase = VerifiedEmailUseCase(user_repo, token_service)
    result = usecase.execute(raw_token)

    assert result["message"] == ERROR_MESSAGES["EMAIL_VERIFIED_SUCCESS"]
    token_service.verify_token.assert_called_once_with(raw_token)
    user_repo.get_verified_email_token.assert_called_once_with(payload["email"])
    token_service.match_token_hash.assert_called_once_with(raw_token, stored_token.token_hash)
    user_repo.confirm_email.assert_called_once_with(email_id=stored_token.email_id, token_id=stored_token.id)


def test_missing_verification_token_raises_error(setup_dependencies):
    user_repo, token_service = setup_dependencies
    usecase = VerifiedEmailUseCase(user_repo, token_service)

    with pytest.raises(ValueError) as exc:
        usecase.execute("")
    assert str(exc.value) == ERROR_MESSAGES["MISSING_VERIFICATION_TOKEN"]


def test_invalid_or_expired_token_raises_error(setup_dependencies):
    user_repo, token_service = setup_dependencies
    token_service.verify_token.return_value = None

    usecase = VerifiedEmailUseCase(user_repo, token_service)
    with pytest.raises(ValueError) as exc:
        usecase.execute("invalid_token")
    assert str(exc.value) == ERROR_MESSAGES["INVALID_OR_EXPIRED_TOKEN"]


def test_invalid_token_type_raises_error(setup_dependencies):
    user_repo, token_service = setup_dependencies
    token_service.verify_token.return_value = {
        "email": "test@example.com",
        "user_id": 1,
        "type": "reset_password"
    }

    usecase = VerifiedEmailUseCase(user_repo, token_service)
    with pytest.raises(ValueError) as exc:
        usecase.execute("token")
    assert str(exc.value) == ERROR_MESSAGES["INVALID_TOKEN_TYPE"]


def test_missing_token_data_raises_error(setup_dependencies):
    user_repo, token_service = setup_dependencies
    token_service.verify_token.return_value = {
        "email": "",
        "user_id": None,
        "type": "verify_email"
    }

    usecase = VerifiedEmailUseCase(user_repo, token_service)
    with pytest.raises(ValueError) as exc:
        usecase.execute("token")
    assert str(exc.value) == ERROR_MESSAGES["MISSING_TOKEN_DATA"]


def test_verification_token_not_found_raises_error(setup_dependencies):
    user_repo, token_service = setup_dependencies
    token_service.verify_token.return_value = {
        "email": "test@example.com",
        "user_id": 1,
        "type": "verify_email"
    }
    user_repo.get_verified_email_token.return_value = None

    usecase = VerifiedEmailUseCase(user_repo, token_service)
    with pytest.raises(ValueError) as exc:
        usecase.execute("token")
    assert str(exc.value) == ERROR_MESSAGES["VERIFICATION_TOKEN_NOT_FOUND"]


def test_token_mismatch_raises_error(setup_dependencies):
    user_repo, token_service = setup_dependencies
    token_service.verify_token.return_value = {
        "email": "test@example.com",
        "user_id": 1,
        "type": "verify_email"
    }
    user_repo.get_verified_email_token.return_value = MockToken()
    token_service.match_token_hash.return_value = False

    usecase = VerifiedEmailUseCase(user_repo, token_service)
    with pytest.raises(ValueError) as exc:
        usecase.execute("token")
    assert str(exc.value) == ERROR_MESSAGES["TOKEN_MISMATCH"]
