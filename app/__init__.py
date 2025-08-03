from dependency_injector.wiring import Provide, inject
from flask import Flask, g

from .containers import Container
from .infrastructure.database.db_connection import SessionLocal, engine
from .infrastructure.database.models import Base

def create_app():
    app = Flask(__name__)

    # Initialize database
    Base.metadata.create_all(bind=engine)
    
    # Setup container
    container = Container()
    app.container = container
    
    # Database session management
    @app.before_request
    def create_session():
        g.db_session = SessionLocal()
        
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session = g.pop('db_session', None)
        if db_session is not None:
            if exception:
                db_session.rollback()
            db_session.close()
    
    # Initialize wiring - must happen after container creation
    container.init_resources()
    container.wire(modules=[__name__])
    
    # Import controllers after wiring is set up
    from .controllers import home_controller
    app.register_blueprint(home_controller.bp)
    
    return app