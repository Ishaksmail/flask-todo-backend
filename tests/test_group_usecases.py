import pytest
from types import SimpleNamespace
from datetime import datetime, timezone

from app.use_cases.groups.create_group_usecase import CreateGroupUseCase
from app.use_cases.groups.update_group_usecase import UpdateGroupUseCase
from app.use_cases.groups.delete_group_usecase import DeleteGroupUseCase


# ---------------- Fixtures ----------------
@pytest.fixture
def mock_group_repo(mocker):
    return mocker.Mock()


@pytest.fixture
def create_group_usecase(mock_group_repo):
    return CreateGroupUseCase(group_repo=mock_group_repo)


@pytest.fixture
def update_group_usecase(mock_group_repo):
    return UpdateGroupUseCase(group_repo=mock_group_repo)


@pytest.fixture
def delete_group_usecase(mock_group_repo):
    return DeleteGroupUseCase(group_repo=mock_group_repo)


# ---------------- Tests: Create Group ----------------
def test_create_group_success(create_group_usecase, mock_group_repo):
    expected_group = SimpleNamespace(
        id=1,
        name="Work",
        description="Work-related tasks",
        is_deleted=False,
        deleted_at=None,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
        user_id=1,
        tasks=[]
    )

    mock_group_repo.create_group.return_value = expected_group

    result = create_group_usecase.execute("Work", "Work-related tasks", 1)

    assert result.id == 1
    assert result.name == "Work"
    mock_group_repo.create_group.assert_called_once()


# ---------------- Tests: Update Group ----------------
def test_update_group_success(update_group_usecase, mock_group_repo):
    expected_group = SimpleNamespace(
        id=1,
        name="Updated Name",
        description="Updated Description",
        is_deleted=False,
        deleted_at=None,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        user_id=1,
        tasks=[]
    )

    mock_group_repo.update_group.return_value = expected_group

    result = update_group_usecase.execute(1, "Updated Name", "Updated Description")

    assert result.name == "Updated Name"
    assert result.description == "Updated Description"
    mock_group_repo.update_group.assert_called_once()
    

def test_update_group_not_found(update_group_usecase, mock_group_repo):
    mock_group_repo.update_group.return_value = None

    result = update_group_usecase.execute(99, "Non-existent", "No group")

    assert result is None
    mock_group_repo.update_group.assert_called_once()


# ---------------- Tests: Delete Group ----------------
def test_delete_group_success(delete_group_usecase, mock_group_repo):
    mock_group_repo.delete_group.return_value = True

    result = delete_group_usecase.execute(1)

    assert result is True
    mock_group_repo.delete_group.assert_called_once_with(1)


def test_delete_group_not_found(delete_group_usecase, mock_group_repo):
    mock_group_repo.delete_group.return_value = False

    result = delete_group_usecase.execute(99)

    assert result is False
    mock_group_repo.delete_group.assert_called_once_with(99)
