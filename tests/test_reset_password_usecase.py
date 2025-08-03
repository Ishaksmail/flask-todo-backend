import pytest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app.use_cases.users.reset_password_usecase import ResetPasswordUseCase


@pytest.fixture
def mock_user_repo(mocker):
    return mocker.Mock()

@pytest.fixture
def mock_token_service(mocker):
    return mocker.Mock()

@pytest.fixture
def mock_hashing_service(mocker):
    service = mocker.Mock()
    service.hash_password.return_value = "hashed_new_password"
    return service

@pytest.fixture
def usecase(mock_user_repo, mock_token_service, mock_hashing_service):
    return ResetPasswordUseCase(
        user_repo=mock_user_repo,
        token_service=mock_token_service,
        hashing_service=mock_hashing_service
    )


# ✅ اختبار النجاح
def test_reset_password_success(usecase, mock_user_repo, mock_token_service):
    raw_token = "valid_token"
    payload = {"type": "reset_password", "user_id": 1}
    stored_token = SimpleNamespace(
        id=1,
        user_id=1,
        is_used=False,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30)
    )

    mock_token_service.verify_token.return_value = payload
    mock_token_service._hash_token.return_value = "hashed_token"
    mock_user_repo.get_password_reset_token.return_value = stored_token

    updated_user = SimpleNamespace(id=1, password="old_password")
    mock_user_repo.update_password.return_value = updated_user

    confirmed_token = SimpleNamespace(id=1, is_used=True, used_at=datetime.now(timezone.utc))
    mock_user_repo.confirm_password_reset_token.return_value = confirmed_token

    result = usecase.execute(raw_token, "new_secure_password")

    assert result is True
    mock_user_repo.update_password.assert_called_once_with(
        id=1,
        new_password_hashing="hashed_new_password"
    )
    mock_user_repo.confirm_password_reset_token.assert_called_once_with(token_id=1)


# ✅ حالات الخطأ
def test_reset_password_missing_token(usecase):
    with pytest.raises(ValueError, match="رمز إعادة التعيين مفقود"):
        usecase.execute("", "new_password")


def test_reset_password_short_password(usecase):
    with pytest.raises(ValueError, match="كلمة المرور الجديدة غير صالحة"):
        usecase.execute("token", "123")


def test_reset_password_invalid_token(usecase, mock_token_service):
    mock_token_service.verify_token.return_value = None
    with pytest.raises(ValueError, match="رمز إعادة تعيين كلمة المرور غير صالح"):
        usecase.execute("invalid_token", "new_password")


def test_reset_password_wrong_type(usecase, mock_token_service):
    mock_token_service.verify_token.return_value = {"type": "verify_email"}
    with pytest.raises(ValueError, match="نوع التوكن غير صالح"):
        usecase.execute("token", "new_password")


def test_reset_password_token_not_found(usecase, mock_token_service, mock_user_repo):
    mock_token_service.verify_token.return_value = {"type": "reset_password"}
    mock_token_service._hash_token.return_value = "hashed_token"
    mock_user_repo.get_password_reset_token.return_value = None

    with pytest.raises(ValueError, match="لم يتم العثور على رمز صالح"):
        usecase.execute("token", "new_password")


def test_reset_password_token_already_used(usecase, mock_token_service, mock_user_repo):
    mock_token_service.verify_token.return_value = {"type": "reset_password"}
    mock_token_service._hash_token.return_value = "hashed_token"
    stored_token = SimpleNamespace(user_id=1, is_used=True)
    mock_user_repo.get_password_reset_token.return_value = stored_token

    with pytest.raises(ValueError, match="تم استخدام هذا الرمز بالفعل"):
        usecase.execute("token", "new_password")


def test_reset_password_user_not_found(usecase, mock_token_service, mock_user_repo):
    mock_token_service.verify_token.return_value = {"type": "reset_password"}
    mock_token_service._hash_token.return_value = "hashed_token"
    stored_token = SimpleNamespace(user_id=1, is_used=False, expires_at=datetime.now(timezone.utc) + timedelta(minutes=30))
    mock_user_repo.get_password_reset_token.return_value = stored_token

    mock_user_repo.update_password.return_value = None

    with pytest.raises(ValueError, match="المستخدم غير موجود"):
        usecase.execute("token", "new_password")


def test_reset_password_confirm_failed(usecase, mock_token_service, mock_user_repo):
    """حالة فشل تأكيد استخدام التوكن"""
    mock_token_service.verify_token.return_value = {"type": "reset_password"}
    mock_token_service._hash_token.return_value = "hashed_token"
    stored_token = SimpleNamespace(user_id=1, id=1, is_used=False, expires_at=datetime.now(timezone.utc) + timedelta(minutes=30))
    mock_user_repo.get_password_reset_token.return_value = stored_token

    updated_user = SimpleNamespace(id=1, password="old_password")
    mock_user_repo.update_password.return_value = updated_user

    mock_user_repo.confirm_password_reset_token.return_value = None

    with pytest.raises(ValueError, match="لم يتم العثور على الرمز أو تم استخدامه بالفعل"):
        usecase.execute("token", "new_password")
