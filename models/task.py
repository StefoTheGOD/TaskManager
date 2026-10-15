class Task:
    def __init__(self, title, subject, description, deadline, priority):
        self.title = title
        self.subject = subject
        self.description = description
        self.deadline = deadline
        self.priority = priority

    def __str__(self):
        return f"{self.subject}: {self.title} | {self.deadline} | {self.priority}"