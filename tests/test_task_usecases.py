import pytest
from types import SimpleNamespace
from datetime import datetime, timezone

from app.use_cases.tasks.create_task_usecase import CreateTaskUseCase
from app.use_cases.tasks.delete_task_usecase import DeleteTaskUseCase
from app.use_cases.tasks.mark_task_completed_usecase import MarkTaskCompletedUseCase
from app.use_cases.tasks.mark_task_uncompleted_usecase import MarkTaskUncompletedUseCase


# ---------------- Fixtures ----------------
@pytest.fixture
def mock_task_repo(mocker):
    return mocker.Mock()


@pytest.fixture
def create_task_usecase(mock_task_repo):
    return CreateTaskUseCase(task_repository=mock_task_repo)


@pytest.fixture
def delete_task_usecase(mock_task_repo):
    return DeleteTaskUseCase(task_repository=mock_task_repo)


@pytest.fixture
def mark_task_completed_usecase(mock_task_repo):
    return MarkTaskCompletedUseCase(task_repository=mock_task_repo)


@pytest.fixture
def mark_task_uncompleted_usecase(mock_task_repo):
    return MarkTaskUncompletedUseCase(task_repository=mock_task_repo)


# ---------------- Tests: Create Task ----------------
def test_create_task_success(create_task_usecase, mock_task_repo):
    task_entity = SimpleNamespace(
        id=None,
        text="New task",
        is_deleted=False,
        is_completed=False,
        deleted_at=None,
        completed_at=None,
        due_at=None,
        created_at=datetime.now(timezone.utc),
        user_id=1,
        group_id=None
    )

    task_data = vars(task_entity)
    task_data["id"] = 1
    expected_task = SimpleNamespace(**task_data)
    mock_task_repo.create_task.return_value = expected_task

    result = create_task_usecase.execute("New task", 1)

    assert result.id == 1
    assert result.text == "New task"
    mock_task_repo.create_task.assert_called_once()


# ---------------- Tests: Delete Task ----------------
def test_delete_task_success(delete_task_usecase, mock_task_repo):
    mock_task_repo.delete_task.return_value = True

    result = delete_task_usecase.execute(1, 1)

    assert result is True
    mock_task_repo.delete_task.assert_called_once_with(1, 1)


def test_delete_task_not_found(delete_task_usecase, mock_task_repo):
    mock_task_repo.delete_task.return_value = False

    result = delete_task_usecase.execute(99, 1)

    assert result is False
    mock_task_repo.delete_task.assert_called_once_with(99, 1)


# ---------------- Tests: Mark Task Completed ----------------
def test_mark_task_completed_success(mark_task_completed_usecase, mock_task_repo):
    mock_task = SimpleNamespace(
        id=1,
        text="Test task",
        is_completed=True,
        completed_at=datetime.now(timezone.utc)
    )
    mock_task_repo.mark_task_completed.return_value = mock_task

    result = mark_task_completed_usecase.execute(1, 1)

    assert result.is_completed is True
    mock_task_repo.mark_task_completed.assert_called_once_with(1, 1)


def test_mark_task_completed_not_found(mark_task_completed_usecase, mock_task_repo):
    mock_task_repo.mark_task_completed.return_value = None

    result = mark_task_completed_usecase.execute(99, 1)

    assert result is None
    mock_task_repo.mark_task_completed.assert_called_once_with(99, 1)


# ---------------- Tests: Mark Task Uncompleted ----------------
def test_mark_task_uncompleted_success(mark_task_uncompleted_usecase, mock_task_repo):
    mock_task = SimpleNamespace(
        id=1,
        text="Test task",
        is_completed=False,
        completed_at=None
    )
    mock_task_repo.mark_task_uncompleted.return_value = mock_task

    result = mark_task_uncompleted_usecase.execute(1, 1)

    assert result.is_completed is False
    mock_task_repo.mark_task_uncompleted.assert_called_once_with(1, 1)


def test_mark_task_uncompleted_not_found(mark_task_uncompleted_usecase, mock_task_repo):
    mock_task_repo.mark_task_uncompleted.return_value = None

    result = mark_task_uncompleted_usecase.execute(99, 1)

    assert result is None
    mock_task_repo.mark_task_uncompleted.assert_called_once_with(99, 1)
