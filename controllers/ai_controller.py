
from flask import Blueprint, render_template, request
from factories.ai_factory import AIFactory
from repositories.task_repository import TaskRepository

ai_controller = Blueprint("ai", __name__)

repository = TaskRepository()
ai_service = AIFactory.create_ai_service("ollama")


@ai_controller.route("/ai-assistant", methods=["GET", "POST"])
def assistant():
    answer = None
    question = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if question:
            tasks = repository.get_all_tasks()

            answer = ai_service.generate_response(
                user_message=question,
                tasks=tasks
            )

    return render_template(
        "ai_assistant.html",
        answer=answer,
        question=question
    )


