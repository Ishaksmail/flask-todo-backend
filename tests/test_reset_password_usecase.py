import pytest
from unittest.mock import MagicMock
from app.use_cases.users.reset_password_usecase import ResetPasswordUseCase
from app.constants.error_messages import ERROR_MESSAGES


class MockToken:
    def __init__(self, id=1, user_id=10, is_used=False):
        self.id = id
        self.user_id = user_id
        self.is_used = is_used


@pytest.fixture
def setup_dependencies():
    user_repo = MagicMock()
    token_service = MagicMock()
    hashing_service = MagicMock()

    return user_repo, token_service, hashing_service


def test_reset_password_success(setup_dependencies):
    user_repo, token_service, hashing_service = setup_dependencies

    token_service.verify_token.return_value = {"type": "reset_password", "user_id": 10}
    token_service._hash_token.return_value = "hashed_token_123"
    user_repo.get_password_reset_token.return_value = MockToken()
    hashing_service.hash_password.return_value = "hashed_new_password"
    user_repo.update_password.return_value = {"id": 10}
    user_repo.confirm_password_reset_token.return_value = True

    usecase = ResetPasswordUseCase(user_repo, token_service, hashing_service)
    result = usecase.execute("valid_raw_token", "NewPassword123")

    assert result is True
    token_service.verify_token.assert_called_once_with("valid_raw_token")
    hashing_service.hash_password.assert_called_once_with("NewPassword123")
    user_repo.update_password.assert_called_once()
    user_repo.confirm_password_reset_token.assert_called_once()


def test_missing_token_raises_error(setup_dependencies):
    user_repo, token_service, hashing_service = setup_dependencies
    usecase = ResetPasswordUseCase(user_repo, token_service, hashing_service)

    with pytest.raises(ValueError) as exc:
        usecase.execute("", "NewPassword123")
    assert str(exc.value) == ERROR_MESSAGES["MISSING_RESET_TOKEN"]


def test_invalid_new_password_raises_error(setup_dependencies):
    user_repo, token_service, hashing_service = setup_dependencies
    usecase = ResetPasswordUseCase(user_repo, token_service, hashing_service)

    with pytest.raises(ValueError) as exc:
        usecase.execute("valid_token", "short")
    assert str(exc.value) == ERROR_MESSAGES["INVALID_NEW_PASSWORD"]


def test_invalid_or_expired_token_raises_error(setup_dependencies):
    user_repo, token_service, hashing_service = setup_dependencies
    token_service.verify_token.return_value = None

    usecase = ResetPasswordUseCase(user_repo, token_service, hashing_service)

    with pytest.raises(ValueError) as exc:
        usecase.execute("expired_token", "ValidPass123")
    assert str(exc.value) == ERROR_MESSAGES["INVALID_OR_EXPIRED_TOKEN"]


def test_invalid_token_type_raises_error(setup_dependencies):
    user_repo, token_service, hashing_service = setup_dependencies
    token_service.verify_token.return_value = {"type": "wrong_type"}

    usecase = ResetPasswordUseCase(user_repo, token_service, hashing_service)

    with pytest.raises(ValueError) as exc:
        usecase.execute("valid_token", "ValidPass123")
    assert str(exc.value) == ERROR_MESSAGES["INVALID_TOKEN_TYPE"]


def test_token_not_found_raises_error(setup_dependencies):
    user_repo, token_service, hashing_service = setup_dependencies
    token_service.verify_token.return_value = {"type": "reset_password"}
    token_service._hash_token.return_value = "hashed_token_123"
    user_repo.get_password_reset_token.return_value = None

    usecase = ResetPasswordUseCase(user_repo, token_service, hashing_service)

    with pytest.raises(ValueError) as exc:
        usecase.execute("valid_token", "ValidPass123")
    assert str(exc.value) == ERROR_MESSAGES["TOKEN_NOT_FOUND"]


def test_token_already_used_raises_error(setup_dependencies):
    user_repo, token_service, hashing_service = setup_dependencies
    token_service.verify_token.return_value = {"type": "reset_password"}
    token_service._hash_token.return_value = "hashed_token_123"
    user_repo.get_password_reset_token.return_value = MockToken(is_used=True)

    usecase = ResetPasswordUseCase(user_repo, token_service, hashing_service)

    with pytest.raises(ValueError) as exc:
        usecase.execute("valid_token", "ValidPass123")
    assert str(exc.value) == ERROR_MESSAGES["TOKEN_ALREADY_USED"]


def test_user_not_found_raises_error(setup_dependencies):
    user_repo, token_service, hashing_service = setup_dependencies
    token_service.verify_token.return_value = {"type": "reset_password"}
    token_service._hash_token.return_value = "hashed_token_123"
    user_repo.get_password_reset_token.return_value = MockToken()
    hashing_service.hash_password.return_value = "hashed_new_password"
    user_repo.update_password.return_value = None

    usecase = ResetPasswordUseCase(user_repo, token_service, hashing_service)

    with pytest.raises(ValueError) as exc:
        usecase.execute("valid_token", "ValidPass123")
    assert str(exc.value) == ERROR_MESSAGES["USER_NOT_FOUND"]


def test_token_confirmation_failed_raises_error(setup_dependencies):
    user_repo, token_service, hashing_service = setup_dependencies
    token_service.verify_token.return_value = {"type": "reset_password"}
    token_service._hash_token.return_value = "hashed_token_123"
    user_repo.get_password_reset_token.return_value = MockToken()
    hashing_service.hash_password.return_value = "hashed_new_password"
    user_repo.update_password.return_value = {"id": 10}
    user_repo.confirm_password_reset_token.return_value = None

    usecase = ResetPasswordUseCase(user_repo, token_service, hashing_service)

    with pytest.raises(ValueError) as exc:
        usecase.execute("valid_token", "ValidPass123")
    assert str(exc.value) == ERROR_MESSAGES["TOKEN_CONFIRMATION_FAILED"]
