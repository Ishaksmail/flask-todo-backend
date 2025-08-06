from app.constants.error_messages import ERROR_MESSAGES
from app.constants.success_messages import SUCCESS_MESSAGES
from app.containers import Container
# use cases
from app.use_cases.tasks.create_task_usecase import CreateTaskUseCase
from app.use_cases.tasks.delete_task_usecase import DeleteTaskUseCase
from app.use_cases.tasks.get_tasks_usecase import GetTaskUseCase
from app.use_cases.tasks.mark_task_completed_usecase import \
    MarkTaskCompletedUseCase
from app.use_cases.tasks.mark_task_uncompleted_usecase import \
    MarkTaskUncompletedUseCase
# flask
from dependency_injector.wiring import Provide, inject
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from ._decorator import handle_api_exceptions

task_bp = Blueprint('task', __name__, url_prefix='/api/task')


@task_bp.route("/", methods=["POST"])
@inject
@jwt_required()
@handle_api_exceptions
def create_task(create_usecase: CreateTaskUseCase = Provide[Container.create_task_usecase]):
    """إضافة مهمة جديدة"""
    data = request.get_json()
    
    user_id = get_jwt()['user_id']

    text = data.get("text")
    group_id = data.get("group_id")
    due_at = data.get("due_at")
    
    if not user_id:
        return jsonify({"done": False, "message": ERROR_MESSAGES["USER_ID_REQUIRED"]}), 400

    if not text:
        return jsonify({"done": False, "message": ERROR_MESSAGES["MISSING_FIELDS"]}), 400

    task = create_usecase.execute(text=text, user_id=user_id, group_id=group_id, due_at=due_at)

    return jsonify(task.__dict__), 201
    
@task_bp.route("/", methods=["GET"])
@inject
@jwt_required()
@handle_api_exceptions
def get_all_tasks(get_usecase: GetTaskUseCase = Provide[Container.get_task_usecase]):
    """جلب جميع المجموعات للمستخدم"""
    
    user_id = get_jwt()['user_id']

    if not user_id:
        return jsonify({"done": False, "message": ERROR_MESSAGES["USER_ID_REQUIRED"]}), 400

    tasks = get_usecase.get_all_tasks(user_id)
    return jsonify([task.__dict__ for task in tasks]), 200



@task_bp.route("/<int:task_id>", methods=["DELETE"])
@inject
@jwt_required()
@handle_api_exceptions
def delete_task(task_id, delete_usecase: DeleteTaskUseCase = Provide[Container.delete_task_usecase]):
    """حذف مهمة"""
    user_id = get_jwt()['user_id']
     
    if not user_id:
        return jsonify({"done": False, "message": ERROR_MESSAGES["USER_ID_REQUIRED"]}), 400

    deleted = delete_usecase.execute(task_id=task_id, user_id=user_id)
    if not deleted:
        return jsonify({"done": False, "message": ERROR_MESSAGES["TASK_NOT_FOUND"]}), 404

    return jsonify({"done": True, "message": SUCCESS_MESSAGES["TASK_DELETED_SUCCESS"]}), 200


@task_bp.route("/complete/<int:task_id>", methods=["PATCH"])
@inject
@jwt_required()
@handle_api_exceptions
def mark_task_completed(task_id, mark_usecase: MarkTaskCompletedUseCase = Provide[Container.mark_task_completed_usecase]):
    """تحديد المهمة كمكتملة"""
    user_id = get_jwt()['user_id']
    
    if not user_id:
        return jsonify({"done": False, "message": ERROR_MESSAGES["USER_ID_REQUIRED"]}), 400

    task = mark_usecase.execute(task_id=task_id, user_id=user_id)
    if not task:
        return jsonify({"done": False, "message": ERROR_MESSAGES["TASK_NOT_FOUND"]}), 404

    return jsonify(task.__dict__), 200


@task_bp.route("/uncomplete/<int:task_id>", methods=["PATCH"])
@inject
@jwt_required()
@handle_api_exceptions
def mark_task_uncompleted(task_id, mark_usecase: MarkTaskUncompletedUseCase = Provide[Container.mark_task_uncompleted_usecase]):
    """إلغاء تحديد المهمة كمكتملة"""
    
    user_id = get_jwt()['user_id']
    
    if not user_id:
        return jsonify({"done": False, "message": ERROR_MESSAGES["USER_ID_REQUIRED"]}), 400

    task = mark_usecase.execute(task_id=task_id, user_id=user_id)
    if not task:
        return jsonify({"done": False, "message": ERROR_MESSAGES["TASK_NOT_FOUND"]}), 404

    return jsonify(task.__dict__), 200
