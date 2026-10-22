
import sqlite3
from pathlib import Path
from threading import Lock
from contextlib import contextmanager


class Database:
    # Singleton Design Pattern
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, "db_path"):
            self.db_path = (
                Path(__file__).resolve().parent.parent
                / "student_planner.db"
            )

    @contextmanager
    def get_connection(self):
        connection = sqlite3.connect(
            self.db_path,
            timeout=10
        )

        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def create_table(self):
        with self.get_connection() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    description TEXT,
                    deadline TEXT,
                    priority TEXT
                )
            """)

    def insert_task(self, task):
        with self.get_connection() as connection:
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

    def select_tasks_by_subject(self, subject):
        with self.get_connection() as connection:
            cursor = connection.execute("""
                SELECT *
                FROM tasks
                WHERE subject = ?
            """, (subject,))

            return cursor.fetchall()

    def select_tasks_by_priority(self, priority):
        with self.get_connection() as connection:
            cursor = connection.execute("""
                SELECT *
                FROM tasks
                WHERE priority = ?
            """, (priority,))

            return cursor.fetchall()



