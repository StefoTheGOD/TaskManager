from database.database import Database


class TaskRepository:
    # Repository Design Pattern

    def __init__(self):
        self.db = Database()

    def get_all_tasks(self):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
        return cursor.fetchall()

    def get_task_by_id(self, task_id):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return cursor.fetchone()

    def insert_task(self, task):
        cursor = self.db.connection.cursor()

        cursor.execute("""
            INSERT INTO tasks (title, subject, description, deadline, priority)
            VALUES (?, ?, ?, ?, ?)
        """, (
            task.title,
            task.subject,
            task.description,
            task.deadline,
            task.priority
        ))

        self.db.connection.commit()

    def update_task(self, task_id, task):
        cursor = self.db.connection.cursor()

        cursor.execute("""
            UPDATE tasks
            SET title = ?, subject = ?, description = ?,
                deadline = ?, priority = ?
            WHERE id = ?
        """, (
            task.title,
            task.subject,
            task.description,
            task.deadline,
            task.priority,
            task_id
        ))

        self.db.connection.commit()

    def delete_task(self, task_id):
        cursor = self.db.connection.cursor()

        cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        self.db.connection.commit()

    def filter_tasks(self, subject="", priority=""):
        cursor = self.db.connection.cursor()

        query = "SELECT * FROM tasks WHERE 1=1"
        parameters = []

        if subject:
            query += " AND subject LIKE ?"
            parameters.append(f"%{subject}%")

        if priority:
            query += " AND priority = ?"
            parameters.append(priority)

        query += " ORDER BY id DESC"

        cursor.execute(query, parameters)

        return cursor.fetchall()

