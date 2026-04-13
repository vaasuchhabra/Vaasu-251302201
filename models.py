import json
from datetime import datetime

class Task:
    """
    Represents a single task in the system.
    """
    PRIORITIES = ["High", "Medium", "Low"]

    def __init__(self, task_id, title, priority, due_date, category, 
                 completed=False, created_at=None):
        self.id = task_id
        self.title = title
        self.priority = priority.capitalize() if priority else "Medium"
        self.due_date = due_date
        self.category = category.capitalize() if category else "General"
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Converts task object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "due_date": self.due_date,
            "category": self.category,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Task object from a dictionary."""
        return cls(
            task_id=data["id"],
            title=data["title"],
            priority=data["priority"],
            due_date=data["due_date"],
            category=data["category"],
            completed=data["completed"],
            created_at=data["created_at"]
        )

    def is_overdue(self):
        """Checks if the task is past its due date and not completed."""
        if self.completed:
            return False
        try:
            today = datetime.now().date()
            due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
            return due < today
        except (ValueError, TypeError):
            return False

    def is_due_today(self):
        """Checks if the task's due date is today."""
        try:
            today = datetime.now().date()
            due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
            return due == today
        except (ValueError, TypeError):
            return False

    def __str__(self):
        status = "✔️" if self.completed else "❌"
        return f"ID: {self.id} | [{status}] {self.title} ({self.priority}) | Due: {self.due_date}"
