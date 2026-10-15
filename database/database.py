import sqlite3


class Database:
    # Singleton Design Pattern
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, "connection"):
            self.connection = sqlite3.connect(
                "student_planner.db",
                check_same_thread=False
            )

    def create_table(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subject TEXT NOT NULL,
                description TEXT,
                deadline TEXT,
                priority TEXT
            )
        """)

        self.connection.commit()

    def insert_task(self, task):
        cursor = self.connection.cursor()

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

        self.connection.commit()

    def select_tasks_by_subject(self, subject):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT *
            FROM tasks
            WHERE subject = ?
        """, (subject,))

        return cursor.fetchall()

    def select_tasks_by_priority(self, priority):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT *
            FROM tasks
            WHERE priority = ?
        """, (priority,))

        return cursor.fetchall()