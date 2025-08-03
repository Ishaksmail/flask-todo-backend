import pytest
from types import SimpleNamespace
from app.use_cases.users.reset_username_usecase import ResetUsernameUseCase


@pytest.fixture
def mock_user_repo(mocker):
    return mocker.Mock()


@pytest.fixture
def usecase(mock_user_repo):
    return ResetUsernameUseCase(user_repo=mock_user_repo)


def test_reset_username_success(usecase, mock_user_repo):
    """يجب أن ينجح تغيير اسم المستخدم عند وجود المستخدم"""
    old_username = "old_user"
    new_username = "new_user"
    updated_user = SimpleNamespace(id=1, username=new_username)

    mock_user_repo.update_username.return_value = updated_user

    result = usecase.execute(old_username, new_username)

    assert result.username == new_username
    mock_user_repo.update_username.assert_called_once_with(
        old_username=old_username,
        new_username=new_username
    )


def test_reset_username_missing_old_username(usecase):
    """يجب أن يفشل عند غياب اسم المستخدم القديم"""
    with pytest.raises(ValueError, match="اسم المستخدم الحالي مفقود"):
        usecase.execute("", "new_user")


def test_reset_username_invalid_new_username(usecase):
    """يجب أن يفشل إذا كان اسم المستخدم الجديد قصيرًا جدًا"""
    with pytest.raises(ValueError, match="اسم المستخدم الجديد غير صالح"):
        usecase.execute("old_user", "ab")


def test_reset_username_user_not_found(usecase, mock_user_repo):
    """يجب أن يفشل إذا لم يتم العثور على المستخدم لتغيير الاسم"""
    mock_user_repo.update_username.return_value = None

    with pytest.raises(ValueError, match="المستخدم غير موجود أو فشل التحديث"):
        usecase.execute("old_user", "new_user")
