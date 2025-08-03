import pytest
from datetime import datetime, timedelta, timezone
from app.use_cases.users.forgot_password_usecase import ForgotPasswordUseCase
from app.domain.entities.password_reset_token_entity import PasswordResetTokenEntity
from app.domain.entities.email_entity import EmailEntity


class FakeUserRepo:
    def __init__(self, email_entity=None):
        self.email_entity = email_entity
        self.token_created = None

    def get_verified_email(self, email_address: str):
        return self.email_entity

    def create_password_reset_token(self, token: PasswordResetTokenEntity):
        self.token_created = token
        return token


class FakeTokenService:
    def generate_token(self, email, user_id, token_type, expires_delta=None):
        return "raw_token_123", "hashed_token_123", datetime.now(timezone.utc) + timedelta(hours=1)


class FakeMailService:
    def __init__(self):
        self.sent_email = None

    def send_email(self, subject, receivers, message):
        self.sent_email = {"subject": subject, "receivers": receivers, "message": message}
        return True


@pytest.fixture
def setup_usecase():
    email_entity = EmailEntity(
        id=1,
        email_address="test@example.com",
        is_primary=True,
        is_deleted=False,
        verified_at=datetime.now(timezone.utc),
        user_id=10
    )
    user_repo = FakeUserRepo(email_entity)
    token_service = FakeTokenService()
    mail_service = FakeMailService()
    return ForgotPasswordUseCase(user_repo, token_service, mail_service, base_url="https://testapp.com"), user_repo, mail_service


def test_forgot_password_success(setup_usecase):
    usecase, user_repo, mail_service = setup_usecase

    response = usecase.execute("test@example.com")

    assert response["message"] == "تم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني"
    assert response["reset_token"] == "raw_token_123"
    assert user_repo.token_created is not None
    assert mail_service.sent_email is not None
    assert "إعادة تعيين كلمة المرور" in mail_service.sent_email["subject"]


def test_forgot_password_no_email_found():
    user_repo = FakeUserRepo(email_entity=None)
    token_service = FakeTokenService()
    mail_service = FakeMailService()
    usecase = ForgotPasswordUseCase(user_repo, token_service, mail_service, base_url="https://testapp.com")

    with pytest.raises(ValueError, match="لا يوجد بريد إلكتروني مؤكد مرتبط بهذا الحساب"):
        usecase.execute("notfound@example.com")


def test_forgot_password_empty_email(setup_usecase):
    usecase, _, _ = setup_usecase

    with pytest.raises(ValueError, match="البريد الإلكتروني مطلوب"):
        usecase.execute("")
