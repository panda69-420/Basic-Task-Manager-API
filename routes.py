from flask import Blueprint, request, jsonify
from models import db, Task

task_routes = Blueprint('task_routes', __name__)

@task_routes.route('/')
def home():
    return "Task API is running 🚀"

# 🔹 GET all tasks
@task_routes.route('/tasks', methods=['GET'])
def get_tasks():
    # 👇 PUT THIS AT THE START
    completed = request.args.get('completed')

    if completed is not None:
        tasks = Task.query.filter_by(
            completed=(completed.lower() == 'true')
        ).all()
    else:
        tasks = Task.query.all()

    return jsonify([task.to_dict() for task in tasks])

# 🔹 POST create task
@task_routes.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()

    # 👇 PUT IT RIGHT HERE
    if not data or not data.get("title"):
        return {"error": "Title is required"}, 400

    # 👇 THEN continue normal logic
    new_task = Task(title=data.get("title"))
    db.session.add(new_task)
    db.session.commit()

    return {
        "message": "Task created",
        "task": new_task.to_dict()
    }, 201

# 🔹 PUT update task
@task_routes.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    if not task:
        return {"error": "Task not found"}, 404

    data = request.get_json()
    task.title = data.get("title", task.title)
    task.completed = data.get("completed", task.completed)

    db.session.commit()

    return {"message": "Task updated"}

# 🔹 DELETE task
@task_routes.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)

    if not task:
        return {"error": "Task not found"}, 404

    db.session.delete(task)
    db.session.commit()

    return {"message": "Task deleted"}
