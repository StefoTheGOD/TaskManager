# TaskManager — Student Task Planner

A student task-management web application built with **Python, Flask and SQLite**. It combines a pastel-colored **Kanban dashboard**, complete task management and a **local AI study assistant** powered by Ollama.

## Features

- **Kanban board** with three statuses: **To Do**, **In Progress**, and **Completed**.
- **Drag and drop** between columns; status changes are saved to SQLite.
- Pastel gradient task cards with colors based on task IDs, so colors remain consistent when tasks move.
- **CRUD** operations: create, view, edit and delete tasks.
- Filter tasks by subject and priority.
- Dashboard counters for total tasks and each status.
- **AI Assistant** that uses saved tasks to help organize studying and prioritize deadlines.
- Responsive interface built with HTML, CSS, JavaScript, Bootstrap and Bootstrap Icons.

## Tech stack

| Layer | Technology |
| --- | --- |
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript, Bootstrap 5 |
| Local AI | Ollama, `qwen2.5:3b` |
| Version control | Git and GitHub |

## Architecture and design patterns

The project follows an **MVC-inspired architecture** with Flask Blueprints:

- **Model:** `models/task.py` — task data model.
- **Views:** `templates/` — HTML pages rendered with Jinja2.
- **Controllers:** `controllers/task_controller.py` and `controllers/ai_controller.py` — request handling and routing.
- **Repository:** `repositories/task_repository.py` — SQLite data operations.
- **Service:** `services/ai_service.py` — Ollama HTTP API integration.

Three design patterns are implemented:

1. **Singleton** — `database/database.py`: one `Database` manager instance, with a separate SQLite connection per operation.
2. **Repository** — `repositories/task_repository.py`: isolates database queries from controllers.
3. **Factory** — `factories/ai_factory.py`: creates an Ollama AI service or a mock service for testing.

## Project structure

```text
TaskManager/
├── controllers/
│   ├── ai_controller.py
│   └── task_controller.py
├── database/
│   └── database.py
├── factories/
│   └── ai_factory.py
├── models/
│   └── task.py
├── repositories/
│   └── task_repository.py
├── services/
│   └── ai_service.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── ai_assistant.html
│   ├── create.html
│   ├── delete.html
│   ├── details.html
│   ├── edit.html
│   └── index.html
├── .gitignore
├── main.py
└── requirements.txt
```

The SQLite file `student_planner.db` is created locally when the application starts and is intentionally excluded from Git.

## Getting started

### 1. Prerequisites

- Python installed on your computer.
- Git (to clone the repository).
- Ollama installed and running **if you want to use the AI Assistant**.

### 2. Clone the repository

```bash
git clone https://github.com/Vladimir-Kralq/ST2-2026-Team-9-TaskManager.git
cd ST2-2026-Team-9-TaskManager
```

### 3. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure local AI (optional for task management)

Install [Ollama](https://ollama.com/), then download the model:

```bash
ollama pull qwen2.5:3b
```

Make sure the Ollama application/service is running. The AI service expects the local API at `http://localhost:11434/api/generate` and the model `qwen2.5:3b`.

> The AI model is **not** included in the GitHub repository. The AI Assistant requires a running local Ollama instance; task management works independently.

### 6. Run the application

```bash
python main.py
```

Open **http://127.0.0.1:5000** in your browser.

On startup, the app creates the `tasks` table if needed. Existing databases without a `status` column are migrated automatically; existing tasks receive the default status **To Do**.

## How to use

1. Click **New Task** to add a title, subject, description, deadline and priority.
2. Manage tasks from the dashboard using **Details**, **Edit** and **Delete**.
3. Move a task between **To Do**, **In Progress** and **Completed** by dragging it to another column or using **Move to**.
4. Use the search field and priority filter to narrow down tasks.
5. Open **AI Assistant** and ask for a study plan or help prioritizing saved tasks.

## Database

The `tasks` table stores:

| Column | Purpose |
| --- | --- |
| `id` | Unique task identifier |
| `title` | Task title |
| `subject` | School/university subject |
| `description` | Task description |
| `deadline` | Due date |
| `priority` | Low, Medium or High |
| `status` | To Do, In Progress or Completed |

## AI integration

The AI Assistant retrieves tasks from SQLite and sends their details, together with the user's question, to the local **Ollama API**. The `OllamaAIService` returns the model's response for display in the web interface. The assistant is instructed to respond in Bulgarian and consider deadlines and priorities.

The **Factory Pattern** also supports a mock provider, useful for testing without running Ollama.

## Development milestones

- **Week 1:** SQLite setup, task model and Singleton pattern.
- **Week 2:** Flask MVC, CRUD and Repository pattern.
- **Week 3:** Details view, modern UI and improved SQLite connection handling.
- **Week 4:** Ollama AI Assistant and Factory pattern.
- **Week 5:** Planora-inspired Kanban dashboard, task statuses, drag-and-drop and pastel card design.

## Notes

- This is a university coursework project.
- Flask's development server (`debug=True` in `main.py`) is intended for local development, not production deployment.
- AI responses are generated by a local language model and may require verification.
