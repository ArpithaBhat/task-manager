from flask import Blueprint, request, jsonify
from Services.task_manager import TaskManager

# Create the blueprint
task_api = Blueprint('task_api', __name__)
manager = TaskManager()

# Route to create a task
@task_api.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = manager.add_task(data['title'])
    return jsonify(task.to_dict()), 201

# Route to get all tasks
@task_api.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = [task.to_dict() for task in manager.get_all_tasks()]
    return jsonify(tasks)

# Route to mark task complete
@task_api.route('/tasks/<int:task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    task = manager.mark_task_complete(task_id)
    if task:
        return jsonify(task.to_dict())
    return jsonify({"error": "Task not found"}), 404

# Route to delete a task
@task_api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if manager.delete_task(task_id):
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404
