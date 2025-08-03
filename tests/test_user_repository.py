# tests/test_user_repository.py
from app.repositories.user_repository import UserRepository
from app.domain.entities.user_entity import UserEntity
from app.domain.entities.email_entity import EmailEntity

def test_create_and_get_user(db_session):
    repo = UserRepository(db_session)
    user = UserEntity(
        id=None,
        username="testuser",
        password="hashedpassword",
        created_at=None,
        emails=[EmailEntity(
            id=None,
            email_address="test@example.com",
            is_primary=True,
            is_deleted=False,
            deleted_at=None,
            verified_at=None,
            user_id=None
        )]
    )

    created_user = repo.create_user(user)
    assert created_user.id is not None

    fetched_user = repo.get_user("testuser")
    assert fetched_user.username == "testuser"
    assert fetched_user.emails[0].email_address == "test@example.com"
