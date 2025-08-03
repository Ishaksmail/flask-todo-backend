# tests/test_group_repository.py
from app.repositories.group_repository import GroupRepository
from app.domain.entities.group_entity import GroupEntity

def test_create_and_get_group(db_session):
    repo = GroupRepository(db_session)
    group = GroupEntity(
        id=None,
        name="My Group",
        description="Test group",
        user_id=1,
        created_at=None,
        updated_at=None,
        deleted_at=None,
        is_deleted=False,
        tasks=[]
    )

    # إنشاء مجموعة
    created_group = repo.create_group(group)
    assert created_group.id is not None
    assert created_group.name == "My Group"

    # جلب المجموعات
    groups = repo.get_groups(user_id=1)
    assert len(groups) == 1
    assert groups[0].name == "My Group"


def test_delete_group(db_session):
    repo = GroupRepository(db_session)
    group = GroupEntity(
        id=None,
        name="Group to Delete",
        description="Testing delete",
        user_id=1,
        created_at=None,
        updated_at=None,
        deleted_at=None,
        is_deleted=False,
        tasks=[]
    )
    created_group = repo.create_group(group)

    result = repo.delete_group(created_group.id)
    assert result is True
