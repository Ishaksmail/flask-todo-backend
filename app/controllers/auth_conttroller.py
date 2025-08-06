from dependency_injector.wiring import Provide, inject
from flask import Blueprint, jsonify
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity,get_jwt, jwt_required,
                                set_access_cookies, set_refresh_cookies,
                                unset_jwt_cookies)
from webargs.flaskparser import use_args

from ..constants.error_messages import ERROR_MESSAGES
from ..constants.success_messages import SUCCESS_MESSAGES
from ..containers import Container
from ..schemas.auth_schemas import *
from ..use_cases.users.login_usecase import LoginUseCase
from ..use_cases.users.register_user_usecase import RegisterUserUseCase
from ._decorator import handle_api_exceptions

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route("/register", methods=["POST"])
@inject
@use_args(RegistrationSchema(), location="json")
@handle_api_exceptions
def register(args, register_usecase: RegisterUserUseCase = Provide[Container.register_user_usecase]):
    user = register_usecase.execute(
        username=args["username"],
        email=args["email"],
        password=args["password"]
    )

    return jsonify({
        "done": True,
        "message": SUCCESS_MESSAGES["USER_REGISTERED_SUCCESS"],
        "user_id": user.id
    }), 201


@auth_bp.route("/login", methods=["POST"])
@inject

@use_args(LoginSchema(), location="json")
@handle_api_exceptions
def login(args, login_usecase: LoginUseCase = Provide[Container.login_usecase]):
    
    
    print('================================')
    
    user = login_usecase.execute(
        username=args["username"],
        password=args["password"]
    )
    
    
    access_token = create_access_token(identity=user.username,additional_claims={'user_id':user.id})
    refresh_token = create_refresh_token(identity= user.username,additional_claims={'user_id':user.id})
    
    resp = jsonify({
        "done": True,
        "message": SUCCESS_MESSAGES["LOGIN_SUCCESS"]
    })
    
    
    set_access_cookies(resp, access_token)
    
    set_refresh_cookies(resp, refresh_token)
    
    return resp, 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@handle_api_exceptions
def refresh():
    current_user = get_jwt_identity()
    user_id = get_jwt()['user_id']
    access_token = create_access_token(identity=current_user,additional_claims={'user_id':user_id})
    resp = jsonify({
        "done": True,
        "message": SUCCESS_MESSAGES["TOKEN_REFRESHED_SUCCESS"]
    })
    set_access_cookies(resp, access_token)
    return resp, 200


@auth_bp.route("/logout", methods=["POST"])
@handle_api_exceptions
def logout():
    resp = jsonify({
        "done": True,
        "message": SUCCESS_MESSAGES["LOGOUT_SUCCESS"]
    })
    unset_jwt_cookies(resp)
    return resp, 200
