from dependency_injector import containers, providers
from .infrastructure.database.db_connection import SessionLocal


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.use_cases",
            "app.services"
        ]
    )
     
    db_session = providers.Singleton(SessionLocal)
