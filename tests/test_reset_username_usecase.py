import pytest
from unittest.mock import MagicMock
from app.use_cases.users.reset_username_usecase import ResetUsernameUseCase
from app.constants.error_messages import ERROR_MESSAGES


@pytest.fixture
def setup_dependencies():
    user_repo = MagicMock()
    return user_repo


def test_reset_username_success(setup_dependencies):
    user_repo = setup_dependencies
    mock_user = {"id": 1, "username": "new_user123"}

    user_repo.update_username.return_value = mock_user

    usecase = ResetUsernameUseCase(user_repo)
    result = usecase.execute("old_user", "new_user123")

    user_repo.update_username.assert_called_once_with(
        old_username="old_user",
        new_username="new_user123"
    )
    assert result["username"] == "new_user123"


def test_missing_old_username_raises_error(setup_dependencies):
    user_repo = setup_dependencies
    usecase = ResetUsernameUseCase(user_repo)

    with pytest.raises(ValueError) as exc:
        usecase.execute("", "new_user123")
    assert str(exc.value) == ERROR_MESSAGES["MISSING_CURRENT_USERNAME"]


def test_invalid_new_username_raises_error(setup_dependencies):
    user_repo = setup_dependencies
    usecase = ResetUsernameUseCase(user_repo)

    with pytest.raises(ValueError) as exc:
        usecase.execute("old_user", "ab")
    assert str(exc.value) == ERROR_MESSAGES["INVALID_NEW_USERNAME"]


def test_username_update_failed_raises_error(setup_dependencies):
    user_repo = setup_dependencies
    user_repo.update_username.return_value = None

    usecase = ResetUsernameUseCase(user_repo)

    with pytest.raises(ValueError) as exc:
        usecase.execute("old_user", "new_user123")
    assert str(exc.value) == ERROR_MESSAGES["USERNAME_UPDATE_FAILED"]
