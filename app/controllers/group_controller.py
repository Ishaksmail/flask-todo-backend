from app.constants.error_messages import ERROR_MESSAGES
from app.constants.success_messages import SUCCESS_MESSAGES
from app.containers import Container
from app.use_cases.groups.create_group_usecase import CreateGroupUseCase
from app.use_cases.groups.delete_group_usecase import DeleteGroupUseCase
from app.use_cases.groups.get_group_usecase import GetGroupUseCase
from app.use_cases.groups.update_group_usecase import UpdateGroupUseCase
from dependency_injector.wiring import Provide, inject
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from ._decorator import handle_api_exceptions

group_bp = Blueprint('group', __name__, url_prefix='/api/group')


@group_bp.route("/", methods=["POST"])
@inject
@jwt_required()
@handle_api_exceptions
def create_group(create_usecase: CreateGroupUseCase = Provide[Container.create_group_usecase]):
    """إنشاء مجموعة جديدة"""
    data = request.get_json()
    
    # استرجاع الهوية من التوكن (تحوي user_id و username)
    current_user = get_jwt_identity()
    user_id = current_user.get("user_id")

    name = data.get("name")
    description = data.get("description")
    
    if not all([name, description, user_id]):
        return jsonify({"done": False, "message": ERROR_MESSAGES["MISSING_FIELDS"]}), 400

    group = create_usecase.execute(name=name, description=description, user_id=user_id)

    return jsonify({
        "done": True,
        "message": SUCCESS_MESSAGES["GROUP_CREATED_SUCCESS"],
        "group_id": group.id
    }), 201


@group_bp.route("/<int:group_id>", methods=["DELETE"])
@inject
@jwt_required()
@handle_api_exceptions
def delete_group(group_id, delete_usecase: DeleteGroupUseCase = Provide[Container.delete_group_usecase]):
    """حذف مجموعة (Soft Delete)"""
    deleted = delete_usecase.execute(group_id)
    if not deleted:
        return jsonify({"done": False, "message": ERROR_MESSAGES["GROUP_NOT_FOUND"]}), 404

    return jsonify({"done": True, "message": SUCCESS_MESSAGES["GROUP_DELETED_SUCCESS"]}), 200


@group_bp.route("/", methods=["GET"])
@inject
@jwt_required()
@handle_api_exceptions
def get_all_groups(get_usecase: GetGroupUseCase = Provide[Container.get_group_usecase]):
    """جلب جميع المجموعات للمستخدم"""
    current_user = get_jwt_identity()
    user_id = current_user.get("user_id")

    if not user_id:
        return jsonify({"done": False, "message": ERROR_MESSAGES["USER_ID_REQUIRED"]}), 400

    groups = get_usecase.get_all_groups(user_id)
    return jsonify([group.__dict__ for group in groups]), 200


@group_bp.route("/completed", methods=["GET"])
@inject
@jwt_required()
@handle_api_exceptions
def get_completed_groups(get_usecase: GetGroupUseCase = Provide[Container.get_group_usecase]):
    """جلب المجموعات المكتملة"""
    current_user = get_jwt_identity()
    user_id = current_user.get("user_id")

    if not user_id:
        return jsonify({"done": False, "message": ERROR_MESSAGES["USER_ID_REQUIRED"]}), 400

    groups = get_usecase.get_completed_groups(user_id)
    return jsonify([group.__dict__ for group in groups]), 200


@group_bp.route("/uncompleted", methods=["GET"])
@inject
@jwt_required()
@handle_api_exceptions
def get_uncompleted_groups(get_usecase: GetGroupUseCase = Provide[Container.get_group_usecase]):
    """جلب المجموعات غير المكتملة"""
    current_user = get_jwt_identity()
    user_id = current_user.get("user_id")

    if not user_id:
        return jsonify({"done": False, "message": ERROR_MESSAGES["USER_ID_REQUIRED"]}), 400

    groups = get_usecase.get_uncompleted_groups(user_id)
    return jsonify([group.__dict__ for group in groups]), 200


@group_bp.route("/<int:group_id>", methods=["PUT"])
@inject
@jwt_required()
@handle_api_exceptions
def update_group(group_id, update_usecase: UpdateGroupUseCase = Provide[Container.update_group_usecase]):
    """تحديث مجموعة"""
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not all([name, description]):
        return jsonify({"done": False, "message": ERROR_MESSAGES["MISSING_FIELDS"]}), 400

    updated_group = update_usecase.execute(group_id=group_id, name=name, description=description)

    if not updated_group:
        return jsonify({"done": False, "message": ERROR_MESSAGES["GROUP_NOT_FOUND"]}), 404

    return jsonify({
        "done": True,
        "message": SUCCESS_MESSAGES["GROUP_UPDATED_SUCCESS"],
        "group_id": updated_group.id
    }), 200
