import csv
import logging
from datetime import datetime
from models import Task
from storage import Storage

class TaskManager:
    """
    Main controller for managing tasks and business logic.
    """
    def __init__(self, storage=None):
        self.storage = storage or Storage()
        self.tasks = self.storage.load_all()
        # logging is configured in main.py
        self.logger = logging.getLogger(__name__)

    def _get_next_id(self):
        """Returns the next available unique ID."""
        if not self.tasks:
            return 1
        return max(t.id for t in self.tasks) + 1

    def add_task(self, title, priority, due_date, category):
        """Creates and saves a new task."""
        new_id = self._get_next_id()
        task = Task(new_id, title, priority, due_date, category)
        self.tasks.append(task)
        self.storage.save_all(self.tasks)
        self.logger.info(f"Task Added: ID {new_id}, Title: '{title}'")
        return task

    def get_task_by_id(self, task_id):
        """Returns a task by its ID or None if not found."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id, **kwargs):
        """Updates specific fields of an existing task."""
        task = self.get_task_by_id(task_id)
        if not task:
            self.logger.warning(f"Update Failed: Task {task_id} not found.")
            return False
        
        for key, value in kwargs.items():
            if hasattr(task, key) and value is not None:
                setattr(task, key, value)
        
        self.storage.save_all(self.tasks)
        self.logger.info(f"Task Updated: ID {task_id}")
        return True

    def toggle_complete(self, task_id):
        """Toggles the completion status of a task."""
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = not task.completed
            self.storage.save_all(self.tasks)
            self.logger.info(f"Task Status Toggled: ID {task_id}, Completed: {task.completed}")
            return True
        return False

    def delete_task(self, task_id):
        """Removes a task from the system."""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.storage.save_all(self.tasks)
            self.logger.info(f"Task Deleted: ID {task_id}")
            return True
        return False

    def search_tasks(self, keyword):
        """Search tasks by title or category."""
        keyword = keyword.lower()
        return [t for t in self.tasks if keyword in t.title.lower() or keyword in t.category.lower()]

    def filter_tasks(self, status=None, priority=None, category=None):
        """Filter tasks by various criteria."""
        filtered = self.tasks
        if status is not None:
            filtered = [t for t in filtered if t.completed == (status == "completed")]
        if priority:
            filtered = [t for t in filtered if t.priority.lower() == priority.lower()]
        if category:
            filtered = [t for t in filtered if t.category.lower() == category.lower()]
        return filtered

    def sort_tasks(self, criteria="due_date"):
        """Sort tasks by due_date, priority, or created_at."""
        if criteria == "priority":
            priority_map = {"High": 0, "Medium": 1, "Low": 2}
            self.tasks.sort(key=lambda t: priority_map.get(t.priority, 3))
        elif criteria == "due_date":
            self.tasks.sort(key=lambda t: t.due_date)
        elif criteria == "created_at":
            self.tasks.sort(key=lambda t: t.created_at)
        
        self.storage.save_all(self.tasks)
        self.logger.info(f"Tasks Sorted by: {criteria}")

    def get_analytics(self):
        """Returns a snapshot of task statistics."""
        total = len(self.tasks)
        if total == 0:
            return {"total": 0, "completed": 0, "pending": 0, "percentage": 0, "overdue": 0}
        
        completed = sum(1 for t in self.tasks if t.completed)
        overdue = sum(1 for t in self.tasks if t.is_overdue())
        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "percentage": (completed / total) * 100,
            "overdue": overdue
        }

    def export_to_csv(self, filename="tasks_export.csv"):
        """Exports the task list to a CSV file."""
        if not self.tasks:
            return False
        
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.tasks[0].to_dict().keys())
                writer.writeheader()
                for task in self.tasks:
                    writer.writerow(task.to_dict())
            self.logger.info(f"Exported tasks to {filename}")
            return True
        except IOError as e:
            self.logger.error(f"Export Error: {e}")
            return False
