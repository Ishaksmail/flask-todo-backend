from flask import Blueprint
from dependency_injector.wiring import Provide, inject
from ..containers import Container
from ..repositories.user_repository import UserRepository
from ..repositories.task_repository import TaskRepository
from ..repositories.group_repository import GroupRepository
from ..domain.entities.user_entity import UserEntity
bp = Blueprint('home', __name__)

@bp.route("/")
@inject
def home(
    user_repo: UserRepository = Provide[Container.user_repository],
    task_repo: TaskRepository = Provide[Container.task_repository],
    group_repo: GroupRepository = Provide[Container.group_repository],
):
    user_repo.create_user(UserEntity(username="smaili",password="12345678"))
    return "All repositories working!"