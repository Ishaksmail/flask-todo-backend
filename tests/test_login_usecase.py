import pytest
from datetime import datetime

from app.use_cases.users.login_usecase import LoginUseCase
from app.domain.entities.email_entity import EmailEntity
from app.domain.entities.user_entity import UserEntity


class MockUserRepository:
    def __init__(self, user=None):
        self.user = user

    def get_user(self, username):
        return self.user if self.user and self.user.username == username else None


class MockHashingService:
    def verify_password(self, password, hashed_password):
        return password == "correct_password"


@pytest.fixture
def sample_user():
    return UserEntity(
        id=1,
        username="testuser",
        password="hashed_password",
        created_at=datetime.utcnow(),
        emails=[
            EmailEntity(
                id=1,
                email_address="test@example.com",
                is_primary=True,
                is_deleted=False,
                verified_at=datetime.utcnow(),
                user_id=1
            )
        ]
    )


def test_login_success(sample_user):
    repo = MockUserRepository(user=sample_user)
    hashing = MockHashingService()
    usecase = LoginUseCase(repo, hashing, token_service=None)

    result = usecase.execute("testuser", "correct_password")

    assert result.username == "testuser"
    assert result.id == 1
    assert len(result.emails) == 1
    assert result.emails[0].email_address == "test@example.com"


def test_login_wrong_username(sample_user):
    repo = MockUserRepository(user=sample_user)
    hashing = MockHashingService()
    usecase = LoginUseCase(repo, hashing, token_service=None)

    with pytest.raises(ValueError, match="اسم المستخدم أو كلمة المرور غير صحيحة"):
        usecase.execute("wronguser", "correct_password")


def test_login_wrong_password(sample_user):
    repo = MockUserRepository(user=sample_user)
    hashing = MockHashingService()
    usecase = LoginUseCase(repo, hashing, token_service=None)

    with pytest.raises(ValueError, match="اسم المستخدم أو كلمة المرور غير صحيحة"):
        usecase.execute("testuser", "wrong_password")


def test_login_no_primary_email():
    user = UserEntity(
        id=1,
        username="testuser",
        password="hashed_password",
        created_at=datetime.utcnow(),
        emails=[]  # لا توجد إيميلات
    )
    repo = MockUserRepository(user=user)
    hashing = MockHashingService()
    usecase = LoginUseCase(repo, hashing, token_service=None)

    with pytest.raises(ValueError, match="لا يوجد بريد إلكتروني أساسي نشط"):
        usecase.execute("testuser", "correct_password")


def test_login_email_not_verified(sample_user):
    sample_user.emails[0].verified_at = None
    repo = MockUserRepository(user=sample_user)
    hashing = MockHashingService()
    usecase = LoginUseCase(repo, hashing, token_service=None)

    with pytest.raises(ValueError, match="يجب تأكيد البريد الإلكتروني"):
        usecase.execute("testuser", "correct_password")
