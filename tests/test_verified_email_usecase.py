import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from app.use_cases.users.verified_email_usecase import VerifiedEmailUseCase
from app.domain.entities.verified_email_token_entity import VerifiedEmailTokenEntity


@pytest.fixture
def mock_user_repo():
    return MagicMock()


@pytest.fixture
def mock_token_service():
    return MagicMock()


@pytest.fixture
def verified_email_usecase(mock_user_repo, mock_token_service):
    return VerifiedEmailUseCase(mock_user_repo, mock_token_service)


def test_execute_success(verified_email_usecase, mock_user_repo, mock_token_service):
    # بيانات وهمية
    raw_token = "valid_token"
    payload = {
        "email": "test@example.com",
        "user_id": 1,
        "type": "verify_email",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token_entity = VerifiedEmailTokenEntity(
        id=1,
        token_hash="hashed_token",
        is_used=False,
        expires_at=datetime.utcnow() + timedelta(hours=1),
        created_at=datetime.utcnow(),
        used_at=None,
        email_id=10,
        user_id=1
    )

    # إعداد الموك
    mock_token_service.verify_token.return_value = payload
    mock_user_repo.get_verified_email_token.return_value = token_entity
    mock_token_service.match_token_hash.return_value = True

    # تنفيذ
    result = verified_email_usecase.execute(raw_token)

    # تحقق
    assert result["message"] == "تم تأكيد البريد الإلكتروني بنجاح"
    mock_token_service.verify_token.assert_called_once_with(raw_token)
    mock_user_repo.get_verified_email_token.assert_called_once_with(payload["email"])
    mock_token_service.match_token_hash.assert_called_once()


def test_execute_invalid_token(verified_email_usecase, mock_token_service):
    mock_token_service.verify_token.return_value = None
    with pytest.raises(ValueError, match="رمز التأكيد غير صالح أو منتهي الصلاحية"):
        verified_email_usecase.execute("invalid_token")


def test_execute_wrong_type(verified_email_usecase, mock_token_service):
    mock_token_service.verify_token.return_value = {
        "email": "test@example.com",
        "user_id": 1,
        "type": "reset_password"
    }
    with pytest.raises(ValueError, match="نوع التوكن غير صالح لهذه العملية"):
        verified_email_usecase.execute("token")


def test_execute_no_stored_token(verified_email_usecase, mock_user_repo, mock_token_service):
    payload = {
        "email": "test@example.com",
        "user_id": 1,
        "type": "verify_email"
    }
    mock_token_service.verify_token.return_value = payload
    mock_user_repo.get_verified_email_token.return_value = None

    with pytest.raises(ValueError, match="لم يتم العثور على رمز صالح لهذا البريد الإلكتروني"):
        verified_email_usecase.execute("token")


def test_execute_hash_mismatch(verified_email_usecase, mock_user_repo, mock_token_service):
    payload = {
        "email": "test@example.com",
        "user_id": 1,
        "type": "verify_email"
    }
    token_entity = VerifiedEmailTokenEntity(
        id=1,
        token_hash="wrong_hash",
        is_used=False,
        expires_at=datetime.utcnow() + timedelta(hours=1),
        created_at=datetime.utcnow(),
        used_at=None,
        email_id=10,
        user_id=1
    )
    mock_token_service.verify_token.return_value = payload
    mock_user_repo.get_verified_email_token.return_value = token_entity
    mock_token_service.match_token_hash.return_value = False

    with pytest.raises(ValueError, match="رمز التأكيد لا يطابق السجل المخزن"):
        verified_email_usecase.execute("token")
