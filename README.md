# TODOLIST PRO CLI

A production-quality Task Management System built with Python. This application demonstrates clean architecture, modular OOP design, and robust CLI engineering practices.

## 🚀 Overview

TODOLIST PRO CLI is designed for professionals and students seeking a reliable, maintainable, and feature-rich CLI tool for managing their daily tasks. It features a modular structure that separates business logic, data persistence, and user interface.

## ✨ Features

- **✅ Task Management**: Complete CRUD operations (Create, Read, Update, Delete).
- **🎨 Professional CLI UX**: Colored output for priorities and status tracking.
- **📁 Persistent Storage**: Automatic JSON serialization with version-aware ID management.
- **🔍 Advanced Search & Filter**: Search by keyword or filter by status, priority, and category.
- **📊 Real-time Analytics**: Visual dashboard showing completion rates and overdue tasks.
- **📅 Deadline Handling**: Automatic detection and highlighting of overdue tasks.
- **📄 CSV Export**: Export your task list to a standard CSV file for external use.
- **📝 Logging**: Action-based logging to `todo_app.log` for audit trails.

## 📂 Project Structure

```
todo_app/
├── main.py            # CLI entry point and menu loop
├── models.py          # Task data structure and business models
├── task_manager.py    # Core business logic (CRUD, sort, filter)
├── storage.py         # JSON storage and I/O handling
├── utils.py           # CLI formatting, colors, and input validation
├── tasks.json         # Data file (persistent storage)
└── todo_app.log       # Application logs (generated at runtime)
```

## 🛠️ How to Run

1.  **Navigate** to the project directory:
    ```bash
    cd /home/vaasu-chhabra/Projects/Projects/phython-project
    ```
2.  **Execute** the application:
    ```bash
    python3 main.py
    ```

## 📖 Usage Examples

-   **Add Task**: Select option 1 and follow the prompts. You can leave fields empty to use sensible defaults.
-   **Show Progress**: Select option 9 to see your analytics dashboard and progress bar.
-   **Export Data**: Select option 10 to save your tasks as a `.csv` file.

## 🔮 Future Improvements

-   [ ] **Unit Testing**: Implement `pytest` suite for task manager logic.
-   [ ] **Sync**: Integration with cloud-based storage.
-   [ ] **Web UI**: Develop a Flask/FastAPI frontend using the existing logic modules.

---
*Created by a Senior Python Developer as a showcase project.*
