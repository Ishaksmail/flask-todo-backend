from flask import Flask
from .containers import Container
from .infrastructure.database.db_connection import SessionLocal,engine
from .infrastructure.database.models import Base,User
def create_app():
    app = Flask(__name__)

   
    Base.metadata.create_all(bind=engine)
    
    
    container = Container()
    container.wire(packages=["app"])
    app.container = container
    

    return app
