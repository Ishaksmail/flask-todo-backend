import pytest
from unittest.mock import MagicMock
from datetime import datetime
from app.use_cases.users.register_user_usecase import RegisterUserUseCase
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.email_entity import EmailEntity


@pytest.fixture
def mock_user_repo():
    return MagicMock()

@pytest.fixture
def mock_hashing_service():
    service = MagicMock()
    service.hash_password.return_value = "hashed_password_123"
    return service

@pytest.fixture
def mock_token_service():
    service = MagicMock()
    service.generate_token.return_value = (
        "raw_token_abc",
        "hashed_token_abc",
        datetime.utcnow()
    )
    return service

@pytest.fixture
def mock_mail_service():
    return MagicMock()

@pytest.fixture
def use_case(mock_user_repo, mock_hashing_service, mock_token_service, mock_mail_service):
    return RegisterUserUseCase(
        user_repo=mock_user_repo,
        hashing_service=mock_hashing_service,
        token_service=mock_token_service,
        mail_service=mock_mail_service,
        base_url="https://example.com"
    )

def test_register_user_success(use_case, mock_user_repo, mock_mail_service):
    # إعداد قيمة الإرجاع لـ create_user
    mock_user_repo.create_user.return_value = UserEntity(
        id=1,
        username="testuser",
        password="hashed_password_123",
        created_at=datetime.utcnow(),
        emails=[EmailEntity(id=10, email_address="test@example.com", is_primary=True, user_id=1)]
    )

    result = use_case.execute(
        username="testuser",
        email="test@example.com",
        password="password123"
    )

    # ✅ التحقق من استدعاء الخدمات
    mock_user_repo.create_user.assert_called_once()
    mock_mail_service.send_email.assert_called_once()
    mock_user_repo.create_verified_email_token.assert_called_once()

    # ✅ التحقق من النتيجة النهائية
    assert result["message"] == "تم إنشاء الحساب بنجاح. تحقق من بريدك الإلكتروني لتأكيد الحساب."
    assert result["user_id"] == 1

def test_register_user_missing_fields(use_case):
    with pytest.raises(ValueError):
        use_case.execute(username="", email="test@example.com", password="123")

