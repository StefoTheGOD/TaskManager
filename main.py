
from flask import Flask
from database.database import Database
from controllers.task_controller import task_controller
from controllers.ai_controller import ai_controller

app = Flask(__name__)

db = Database()
db.create_table()

app.register_blueprint(task_controller)
app.register_blueprint(ai_controller)

if __name__ == "__main__":
    app.run(debug=True)


