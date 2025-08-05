import pytest
from types import SimpleNamespace
from app.use_cases.groups.get_group_usecase import GetGroupUseCase
from app.constants.error_messages import ERROR_MESSAGES

@pytest.fixture
def mock_group_repo(mocker):
    return mocker.Mock()


@pytest.fixture
def usecase(mock_group_repo):
    return GetGroupUseCase(group_repo=mock_group_repo)


# ✅ 1) اختبار جلب جميع المجموعات
def test_get_all_groups_success(usecase, mock_group_repo):
    user_id = 1
    expected_groups = [
        SimpleNamespace(id=1, name="Group A"),
        SimpleNamespace(id=2, name="Group B"),
    ]
    mock_group_repo.get_groups.return_value = expected_groups

    result = usecase.get_all_groups(user_id)

    assert result == expected_groups
    mock_group_repo.get_groups.assert_called_once_with(user_id=user_id)


def test_get_all_groups_missing_user_id(usecase):
    with pytest.raises(ValueError, match=ERROR_MESSAGES["USER_ID_REQUIRED"]):
        usecase.get_all_groups(None)


# ✅ 2) اختبار جلب المجموعات المكتملة
def test_get_completed_groups_success(usecase, mock_group_repo):
    user_id = 1
    expected_groups = [SimpleNamespace(id=3, name="Completed Group")]
    mock_group_repo.get_groups_complete.return_value = expected_groups

    result = usecase.get_completed_groups(user_id)

    assert result == expected_groups
    mock_group_repo.get_groups_complete.assert_called_once_with(user_id=user_id)


def test_get_completed_groups_missing_user_id(usecase):
    with pytest.raises(ValueError, match=ERROR_MESSAGES["USER_ID_REQUIRED"]):
        usecase.get_completed_groups(None)


# ✅ 3) اختبار جلب المجموعات غير المكتملة
def test_get_uncompleted_groups_success(usecase, mock_group_repo):
    user_id = 1
    expected_groups = [SimpleNamespace(id=4, name="Uncompleted Group")]
    mock_group_repo.get_groups_uncomplete.return_value = expected_groups

    result = usecase.get_uncompleted_groups(user_id)

    assert result == expected_groups
    mock_group_repo.get_groups_uncomplete.assert_called_once_with(user_id=user_id)


def test_get_uncompleted_groups_missing_user_id(usecase):
    with pytest.raises(ValueError, match=ERROR_MESSAGES["USER_ID_REQUIRED"]):
        usecase.get_uncompleted_groups(None)
