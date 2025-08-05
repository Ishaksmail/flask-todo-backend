import os
from datetime import timedelta

from dependency_injector.wiring import Provide, inject
from dotenv import load_dotenv
from flask import Flask, g, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

# containers
from .containers import Container
# controllers
from .controllers.auth_conttroller import auth_bp
from .controllers.group_controller import group_bp
from .controllers.task_controller import task_bp
from .controllers.user_controller import user_bp
# infrastructure
from .infrastructure.database.db_connection import SessionLocal, engine
from .infrastructure.database.models import Base

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # إعدادات JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = os.getenv('JWT_TOKEN_LOCATION', 'cookies').split(',')
    app.config['JWT_COOKIE_SECURE'] = os.getenv('JWT_COOKIE_SECURE', 'False') == 'True'
    app.config['JWT_COOKIE_HTTPONLY'] = os.getenv('JWT_COOKIE_HTTPONLY')
    app.config['JWT_SESSION_COOKIE'] = os.getenv('JWT_SESSION_COOKIE')
    app.config['JWT_COOKIE_SAMESITE'] = os.getenv('JWT_COOKIE_SAMESITE')
    app.config['JWT_ACCESS_COOKIE_PATH'] = os.getenv('JWT_ACCESS_COOKIE_PATH')
    app.config['JWT_REFRESH_COOKIE_PATH'] = os.getenv('JWT_REFRESH_COOKIE_PATH')
    app.config['JWT_COOKIE_CSRF_PROTECT'] = os.getenv('JWT_COOKIE_CSRF_PROTECT', 'True') == 'True'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = os.getenv('JWT_ACCESS_CSRF_HEADER_NAME')
    app.config['JWT_REFRESH_CSRF_HEADER_NAME'] = os.getenv('JWT_REFRESH_CSRF_HEADER_NAME')
    
    jwt = JWTManager(app)
    
    # إعداد CORS للسماح بالكوكيز بين النطاقات
    CORS(
        app,
        supports_credentials=True,
        expose_headers=["X-CSRF-TOKEN"],
        allow_headers=["X-CSRF-TOKEN", "Content-Type"])
    
    # إنشاء قاعدة البيانات (يمكن تفعيلها عند الحاجة فقط)
    # Base.metadata.create_all(bind=engine)
    
    # إعداد الحاوية
    container = Container()
    app.container = container
    
    # إدارة جلسة قاعدة البيانات
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
    
    # تهيئة الموارد بعد الحاوية
    container.init_resources()
    container.wire(modules=[__name__])
    
    # تسجيل الـ Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(group_bp, url_prefix="/api/group")
    app.register_blueprint(task_bp, url_prefix="/api/task")
    
    from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity,get_jwt

    @app.route("/api/test", methods=["GET", "POST"])
    def test_request():
        details = {
            "method": request.method,
            "cookies": request.cookies,
            "headers": dict(request.headers)
        }
        
        print(details)
        
        identity = None
        try:
            verify_jwt_in_request(optional=True)  # ✅ يجعل التحقق اختياري
            identity = get_jwt_identity()
            id_user = get_jwt()['user_id']
            print(id_user)
        except Exception as e:
            print("JWT Error:", e)
        
        print("===== تفاصيل الطلب =====")
        print("JWT Identity:", identity)
        print("========================")
        return jsonify(details), 200

        
    return app
