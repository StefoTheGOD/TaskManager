from flask import Flask
from database.database import Database
from controllers.task_controller import task_controller


app = Flask(__name__)

# Initialize database
db = Database()
db.create_table()

# Register MVC controller
app.register_blueprint(task_controller)


if __name__ == "__main__":
    app.run(debug=True)

