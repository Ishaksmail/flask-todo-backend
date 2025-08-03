from dependency_injector import containers, providers
from flask import g

from .repositories.group_repository import GroupRepository
from .repositories.task_repository import TaskRepository
from .repositories.user_repository import UserRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[".controllers"])

    db_session = providers.Factory(lambda: g.db_session)     

    
    user_repository = providers.Factory(
        UserRepository,
        session=db_session
    )
    
    task_repository = providers.Factory(
        TaskRepository,
        session=db_session
    )
    
    group_repository = providers.Factory(
        GroupRepository,
        session=db_session
    )