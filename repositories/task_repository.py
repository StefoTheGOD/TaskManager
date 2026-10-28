
from database.database import Database


class TaskRepository:

    # Repository Design Pattern
    VALID_STATUSES = ("To Do", "In Progress", "Completed")

    def __init__(self):
        self.db = Database()

    def get_all_tasks(self):
        with self.db.get_connection() as connection:
            cursor = connection.execute(
                "SELECT * FROM tasks ORDER BY id DESC"
            )
            return cursor.fetchall()

    def get_task_by_id(self, task_id):
        with self.db.get_connection() as connection:
            cursor = connection.execute(
                "SELECT * FROM tasks WHERE id = ?",
                (task_id,)
            )
            return cursor.fetchone()

    def insert_task(self, task):
        with self.db.get_connection() as connection:
            connection.execute("""
                INSERT INTO tasks
                (title, subject, description, deadline, priority)
                VALUES (?, ?, ?, ?, ?)
            """, (
                task.title,
                task.subject,
                task.description,
                task.deadline,
                task.priority
            ))

    def update_task(self, task_id, task):
        with self.db.get_connection() as connection:
            connection.execute("""
                UPDATE tasks
                SET title = ?,
                    subject = ?,
                    description = ?,
                    deadline = ?,
                    priority = ?
                WHERE id = ?
            """, (
                task.title,
                task.subject,
                task.description,
                task.deadline,
                task.priority,
                task_id
            ))

    def delete_task(self, task_id):
        with self.db.get_connection() as connection:
            connection.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,)
            )

    def filter_tasks(self, subject="", priority=""):
        query = "SELECT * FROM tasks WHERE 1=1"
        parameters = []

        if subject:
            query += " AND subject LIKE ?"
            parameters.append(f"%{subject}%")

        if priority:
            query += " AND priority = ?"
            parameters.append(priority)

        query += " ORDER BY id DESC"

        with self.db.get_connection() as connection:
            cursor = connection.execute(
                query,
                parameters
            )
            return cursor.fetchall()

    # Week 5 - Kanban Board

    def get_tasks_by_status(self, status):
        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid task status")

        with self.db.get_connection() as connection:
            cursor = connection.execute("""
                SELECT *
                FROM tasks
                WHERE status = ?
                ORDER BY id DESC
            """, (status,))

            return cursor.fetchall()

    def update_task_status(self, task_id, status):
        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid task status")

        with self.db.get_connection() as connection:
            cursor = connection.execute("""
                UPDATE tasks
                SET status = ?
                WHERE id = ?
            """, (status, task_id))

            return cursor.rowcount > 0



