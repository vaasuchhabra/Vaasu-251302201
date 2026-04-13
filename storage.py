import json
import os
import logging
from models import Task

class Storage:
    """Handles JSON storage for tasks."""

    def __init__(self, filename="tasks.json"):
        self.filename = filename

    def load_all(self):
        """Loads all tasks from the JSON file. Returns a list of Task objects."""
        if not os.path.exists(self.filename):
            logging.info(f"Storage: '{self.filename}' not found. Initializing new task list.")
            return []

        try:
            with open(self.filename, 'r') as f:
                data_list = json.load(f)
                if not isinstance(data_list, list):
                    logging.warning(f"Storage: Corrupted format in '{self.filename}'. Expected list. Returning empty list.")
                    return []
                
                tasks = [Task.from_dict(item) for item in data_list]
                logging.info(f"Storage: Successfully loaded {len(tasks)} tasks.")
                return tasks
        except (json.JSONDecodeError, KeyError, IOError) as e:
            logging.error(f"Storage: Failed to load tasks from {self.filename}: {e}")
            print(f"\n[!] Error loading data file. Starting with an empty list.")
            return []

    def save_all(self, tasks):
        """Saves a list of Task objects to the JSON file."""
        try:
            data_list = [task.to_dict() for task in tasks]
            with open(self.filename, 'w') as f:
                json.dump(data_list, f, indent=4)
            logging.info(f"Storage: Successfully saved {len(tasks)} tasks to {self.filename}.")
        except IOError as e:
            logging.error(f"Storage: Failed to save tasks to {self.filename}: {e}")
            print(f"\n[!] Error saving data file: {e}")
