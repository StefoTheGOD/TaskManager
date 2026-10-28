
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    abort
)

from repositories.task_repository import TaskRepository
from models.task import Task


task_controller = Blueprint("tasks", __name__)
repository = TaskRepository()


@task_controller.route("/")
def index():
    subject = request.args.get("subject", "")
    priority = request.args.get("priority", "")

    tasks = repository.filter_tasks(subject, priority)

    # Week 5 - Kanban columns
    todo_tasks = [
        task for task in tasks
        if task[6] == "To Do"
    ]

    progress_tasks = [
        task for task in tasks
        if task[6] == "In Progress"
    ]

    completed_tasks = [
        task for task in tasks
        if task[6] == "Completed"
    ]

    return render_template(
        "index.html",
        tasks=tasks,
        subject=subject,
        priority=priority,
        todo_tasks=todo_tasks,
        progress_tasks=progress_tasks,
        completed_tasks=completed_tasks
    )


@task_controller.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        task = Task(
            request.form["title"],
            request.form["subject"],
            request.form["description"],
            request.form["deadline"],
            request.form["priority"]
        )

        repository.insert_task(task)

        return redirect(url_for("tasks.index"))

    return render_template("create.html")


@task_controller.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    if request.method == "POST":
        task = Task(
            request.form["title"],
            request.form["subject"],
            request.form["description"],
            request.form["deadline"],
            request.form["priority"]
        )

        repository.update_task(task_id, task)

        return redirect(url_for("tasks.index"))

    task = repository.get_task_by_id(task_id)

    if task is None:
        abort(404)

    return render_template(
        "edit.html",
        task=task
    )


@task_controller.route("/delete/<int:task_id>", methods=["GET", "POST"])
def delete(task_id):
    task = repository.get_task_by_id(task_id)

    if task is None:
        abort(404)

    if request.method == "POST":
        repository.delete_task(task_id)
        return redirect(url_for("tasks.index"))

    return render_template(
        "delete.html",
        task=task
    )


@task_controller.route("/details/<int:task_id>")
def details(task_id):
    task = repository.get_task_by_id(task_id)

    if task is None:
        abort(404)

    return render_template(
        "details.html",
        task=task
    )


# Week 5 - Update task status
@task_controller.route(
    "/task/<int:task_id>/status",
    methods=["POST"]
)
def update_status(task_id):
    status = request.form.get("status", "")

    if status not in repository.VALID_STATUSES:
        abort(400, description="Invalid task status")

    updated = repository.update_task_status(
        task_id,
        status
    )

    if not updated:
        abort(404, description="Task not found")

    return redirect(url_for("tasks.index"))



