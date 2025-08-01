from flask import Flask
from .infrastructure.database.db_connection import SessionLocal,engine
from .infrastructure.database.models import Base,User
def create_app():
    app = Flask(__name__)

   
    Base.metadata.create_all(bind=engine)


    @app.route("/")
    def home():
        session = SessionLocal()
        users = session.query(User).all()
        print(users)
        return "API is running"

    return app
