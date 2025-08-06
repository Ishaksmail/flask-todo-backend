import os

from dependency_injector import containers, providers
from dotenv import load_dotenv
from flask import g

# repos
from .repositories.group_repository import GroupRepository
from .repositories.task_repository import TaskRepository
from .repositories.user_repository import UserRepository
# services
from .services.mail_service import MailService
from .services.password_hashing_service import PasswordHashingService
from .services.token_service import TokenService
# use cases
from .use_cases.groups.create_group_usecase import CreateGroupUseCase
from .use_cases.groups.delete_group_usecase import DeleteGroupUseCase
from .use_cases.groups.get_group_usecase import GetGroupUseCase
from .use_cases.groups.update_group_usecase import UpdateGroupUseCase

from .use_cases.tasks.get_tasks_usecase import GetTaskUseCase
from .use_cases.tasks.create_task_usecase import CreateTaskUseCase
from .use_cases.tasks.delete_task_usecase import DeleteTaskUseCase
from .use_cases.tasks.mark_task_completed_usecase import \
    MarkTaskCompletedUseCase
from .use_cases.tasks.mark_task_uncompleted_usecase import \
    MarkTaskUncompletedUseCase
from .use_cases.users.create_email_usecase import \
    CreateVerifiedEmailTokenUseCase
from .use_cases.users.forgot_password_usecase import ForgotPasswordUseCase
from .use_cases.users.get_user_usecase import GetUserUseCase
from .use_cases.users.login_usecase import LoginUseCase
from .use_cases.users.register_user_usecase import RegisterUserUseCase
from .use_cases.users.reset_password_usecase import ResetPasswordUseCase
from .use_cases.users.reset_username_usecase import ResetUsernameUseCase
from .use_cases.users.verified_email_usecase import VerifiedEmailUseCase

load_dotenv()

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=[".controllers"])

    db_session = providers.Factory(lambda: g.db_session)

    # ========== Repositories ==========

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

    # ========== Services ==========

    mail_service = providers.Singleton(
        MailService,
        host=os.getenv("EMAIL_HOST"),
        port=int(os.getenv("EMAIL_PORT", 587)),
        username=os.getenv("EMAIL_HOST_USER"),
        password=os.getenv("EMAIL_HOST_PASSWORD")
    )

    password_hashing_service = providers.Singleton(
        PasswordHashingService,
        pepper=os.getenv("PASSWORD_PEPPER")
    )

    token_service = providers.Singleton(
        TokenService,
        secret_key=os.getenv("SECRET_KEY"),
        algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        token_expire_minutes=int(os.getenv("JWT_EXPIRE_MINUTES", 30))
    )

    # ========== Use Cases ==========

    # --- Users ---
    
    get_user_usecase = providers.Factory(
        GetUserUseCase,
        user_repo=user_repository
    )
    
    login_usecase = providers.Factory(
        LoginUseCase,
        user_repo=user_repository,
        hashing_service=password_hashing_service,
        token_service=token_service
    )

    register_user_usecase = providers.Factory(
        RegisterUserUseCase,
        user_repo=user_repository,
        hashing_service=password_hashing_service,
        token_service=token_service,
        mail_service=mail_service,
        base_url=os.getenv("APP_BASE_URL", "http://localhost:5000")
    )

    forgot_password_usecase = providers.Factory(
        ForgotPasswordUseCase,
        user_repo=user_repository,
        token_service=token_service,
        mail_service=mail_service,
        base_url=os.getenv("APP_BASE_URL", "http://localhost:5000")
    )
    
    create_verified_email_usecase = providers.Factory(
        CreateVerifiedEmailTokenUseCase,
        user_repo=user_repository,
        token_service=token_service,
        mail_service=mail_service,
        base_url=os.getenv("APP_BASE_URL", "http://localhost:5000")
    )

    reset_password_usecase = providers.Factory(
        ResetPasswordUseCase,
        user_repo=user_repository,
        token_service=token_service,
        hashing_service=password_hashing_service
    )

    reset_username_usecase = providers.Factory(
        ResetUsernameUseCase,
        user_repo=user_repository
    )

    verified_email_usecase = providers.Factory(
        VerifiedEmailUseCase,
        user_repo=user_repository,
        token_service=token_service
    )

    # --- Tasks ---
    create_task_usecase = providers.Factory(
        CreateTaskUseCase,
        task_repository=task_repository
    )

    delete_task_usecase = providers.Factory(
        DeleteTaskUseCase,
        task_repository=task_repository
    )

    mark_task_completed_usecase = providers.Factory(
        MarkTaskCompletedUseCase,
        task_repository=task_repository
    )

    mark_task_uncompleted_usecase = providers.Factory(
        MarkTaskUncompletedUseCase,
        task_repository=task_repository
    )
    
    get_task_usecase = providers.Factory(
        GetTaskUseCase, 
        task_repository=task_repository    
    )

    # --- Groups ---
    create_group_usecase = providers.Factory(
        CreateGroupUseCase, 
        group_repository=group_repository
    )
    
    delete_group_usecase = providers.Factory(
        DeleteGroupUseCase,
        group_repository=group_repository
    )

    get_group_usecase = providers.Factory(
        GetGroupUseCase, 
        group_repository=group_repository
    )

    update_group_usecase = providers.Factory(
        UpdateGroupUseCase, 
        group_repository=group_repository
    )
