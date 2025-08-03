import os

from dependency_injector import containers, providers
from dotenv import load_dotenv
from flask import g

from .repositories.group_repository import GroupRepository
from .repositories.task_repository import TaskRepository
from .repositories.user_repository import UserRepository
from .services.mail_service import MailService
from .services.token_service import TokenService
from .services.password_hashing_service import PasswordHashingService

load_dotenv()

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
    
    mail_service = providers.Singleton(
        MailService,
        host=os.getenv("EMAIL_HOST"),
        port=os.getenv("EMAIL_PORT"),
        username=os.getenv("EMAIL_HOST_USER"),
        password=os.getenv("EMAIL_HOST_PASSWORD")
    )
    
    token_service = providers.Singleton(
        TokenService,
        secret_key=os.getenv("SECRET_KEY"),
        algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        token_expire_minutes=int(os.getenv("JWT_EXPIRE_MINUTES", 30))
    )
    
    
    