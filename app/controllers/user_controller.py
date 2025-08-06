from dependency_injector.wiring import Provide, inject
from flask import current_app, current_app, Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_header, get_jwt, current_user, get_jwt_identity, jwt_required

from app.constants.error_messages import ERROR_MESSAGES
from app.constants.success_messages import SUCCESS_MESSAGES
from app.containers import Container
from app.use_cases.users.forgot_password_usecase import ForgotPasswordUseCase
from app.use_cases.users.reset_password_usecase import ResetPasswordUseCase
from app.use_cases.users.reset_username_usecase import ResetUsernameUseCase
from app.use_cases.users.verified_email_usecase import VerifiedEmailUseCase

from ._decorator import handle_api_exceptions

user_bp = Blueprint('user', __name__, url_prefix='/api/user')


@user_bp.route("/forgot-password", methods=["POST"])
@inject
@handle_api_exceptions
def forgot_password(forgot_usecase: ForgotPasswordUseCase = Provide[Container.forgot_password_usecase]):
    """إرسال رابط إعادة تعيين كلمة المرور"""
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"done": False, "message": ERROR_MESSAGES["EMAIL_REQUIRED"]}), 400

    try:
        result = forgot_usecase.execute(email=email)
        return jsonify({"done": True, "message": result["message"], "reset_token": result["reset_token"]}), 200
    except Exception as e:
        return jsonify({"done": False, "message": str(e)}), 400


@user_bp.route("/reset-password", methods=["POST"])
@inject
@handle_api_exceptions
def reset_password(reset_usecase: ResetPasswordUseCase = Provide[Container.reset_password_usecase]):
    """إعادة تعيين كلمة المرور"""
    data = request.get_json()
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"done": False, "message": ERROR_MESSAGES["MISSING_FIELDS"]}), 400

    try:
        reset_usecase.execute(raw_token=token, new_password=new_password)
        return jsonify({"done": True, "message": SUCCESS_MESSAGES["PASSWORD_RESET_SUCCESS"]}), 200
    except Exception as e:
        return jsonify({"done": False, "message": str(e)}), 400


@user_bp.route("/reset-username", methods=["POST"])
@inject
@jwt_required()
@handle_api_exceptions
def reset_username(reset_username_usecase: ResetUsernameUseCase = Provide[Container.reset_username_usecase]):
    """تغيير اسم المستخدم"""
    data = request.get_json()
    new_username = data.get("new_username")

    current_user = get_jwt_identity()
    user_id = current_user.get("user_id")

    if not user_id or not new_username:
        return jsonify({"done": False, "message": ERROR_MESSAGES["MISSING_FIELDS"]}), 400

    try:
        updated_user = reset_username_usecase.execute(user_id=user_id, new_username=new_username)
        return jsonify({
            "done": True,
            "message": SUCCESS_MESSAGES["USERNAME_RESET_SUCCESS"],
            "new_username": updated_user.username
        }), 200
    except Exception as e:
        return jsonify({"done": False, "message": str(e)}), 400




@user_bp.route("/email", methods=["POST"])
@inject
@jwt_required()
@handle_api_exceptions
def create_email(
    create_email_usecase = Provide[Container.create_verified_email_usecase]
):
    data = request.get_json()

    email_address = data.get("email")
    current_user = get_jwt_identity()
    user_id = current_user["user_id"]

    if not email_address:
        return jsonify({"error": ERROR_MESSAGES["MISSING_EMAIL_ADDRESS"]}), 400
    if not user_id:
        return jsonify({"error": ERROR_MESSAGES["MISSING_USER_ID"]}), 400

    try:
        result = create_email_usecase.execute(
            email_address=email_address,
            user_id=user_id
        )
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": ERROR_MESSAGES["UNKNOWN_ERROR"]}), 500
    

@user_bp.route("/verify-email", methods=["POST"])
@inject
@handle_api_exceptions
def verify_email(verify_email_usecase: VerifiedEmailUseCase = Provide[Container.verified_email_usecase]):
    """تأكيد البريد الإلكتروني"""
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"done": False, "message": ERROR_MESSAGES["MISSING_VERIFICATION_TOKEN"]}), 400

    try:
        result = verify_email_usecase.execute(raw_token=token)
        return jsonify({"done": True, "message": result["message"]}), 200
    except Exception as e:
        return jsonify({"done": False, "message": str(e)}), 400


@user_bp.route("/isLogin", methods=["GET"])
@jwt_required(optional=True)
@inject
def check_login(get_user_usecase=Provide[Container.get_user_usecase]):
    current_user = get_jwt_identity()
    
        
    user = get_user_usecase.execute(username=current_user)
    
    if not user:
        return jsonify({
            "isLoggedIn": False,
            "message": ERROR_MESSAGES["USER_NOT_FOUND"]
        }), 200
    
    
    return jsonify({
        "isLoggedIn": True,
        "message": SUCCESS_MESSAGES["LOGIN_SUCCESS"],
        "username":current_user
    }), 200