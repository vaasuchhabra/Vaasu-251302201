import sys
import logging
from task_manager import TaskManager
from utils import (
    get_input, validate_date, format_task_table, 
    print_message, clear_screen, Colors
)

def setup_logging():
    """Configures the logging system to track application usage."""
    logging.basicConfig(
        filename='todo_app.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def display_menu():
    """Prints the main dashboard menu."""
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}=== TODOLIST PRO CLI ==={Colors.ENDC}")
    print("1.  Add Task")
    print("2.  View All Tasks")
    print("3.  Update Task")
    print("4.  Delete Task")
    print("5.  Mark Complete")
    print("6.  Search Tasks")
    print("7.  Filter Tasks")
    print("8.  Sort Tasks")
    print("9.  Show Analytics")
    print("10. Export to CSV")
    print(f"{Colors.FAIL}11. Exit{Colors.ENDC}")
    print("-" * 25)

def main():
    setup_logging()
    manager = TaskManager()
    
    while True:
        display_menu()
        choice = input("Select an option (1-11): ").strip()

        if choice == "1":
            title = get_input("Task Title")
            priority = get_input("Priority (High/Medium/Low)", default="Medium")
            due_date = get_input("Due Date (YYYY-MM-DD)", validator=validate_date, error_msg="Invalid date format.")
            category = get_input("Category", default="General")
            manager.add_task(title, priority, due_date, category)
            print_message("Task added successfully!", "success")

        elif choice == "2":
            tasks = manager.tasks
            format_task_table(tasks, "ALL TASKS")

        elif choice == "3":
            format_task_table(manager.tasks)
            tid_str = get_input("Enter Task ID to update", validator=lambda x: x.isdigit())
            tid = int(tid_str)
            task = manager.get_task_by_id(tid)
            if task:
                print(f"{Colors.OKCYAN}Editing Task: {task.title} (Press Enter to keep current){Colors.ENDC}")
                new_title = input(f"New Title [{task.title}]: ").strip() or None
                new_priority = input(f"New Priority [{task.priority}]: ").strip() or None
                new_due = input(f"New Due Date [{task.due_date}]: ").strip()
                if new_due and not validate_date(new_due):
                    print_message("Invalid date format. Skipping date update.", "error")
                    new_due = None
                new_cat = input(f"New Category [{task.category}]: ").strip() or None
                
                manager.update_task(tid, title=new_title, priority=new_priority, due_date=new_due, category=new_cat)
                print_message("Task updated!", "success")
            else:
                print_message("Task ID not found.", "error")

        elif choice == "4":
            format_task_table(manager.tasks)
            tid_str = get_input("Enter Task ID to delete", validator=lambda x: x.isdigit())
            if manager.delete_task(int(tid_str)):
                print_message("Task deleted.", "success")
            else:
                print_message("Task not found.", "error")

        elif choice == "5":
            format_task_table(manager.tasks)
            tid_str = get_input("Enter Task ID to toggle complete", validator=lambda x: x.isdigit())
            if manager.toggle_complete(int(tid_str)):
                print_message("Status updated!", "success")
            else:
                print_message("Task not found.", "error")

        elif choice == "6":
            keyword = get_input("Search Keyword (title/category)")
            results = manager.search_tasks(keyword)
            format_task_table(results, f"SEARCH RESULTS: '{keyword}'")

        elif choice == "7":
            print("\nFilter by: 1. Status (Completed) | 2. Status (Pending) | 3. Priority | 4. Category")
            f_choice = input("Select filter type (1-4): ")
            if f_choice == "1":
                format_task_table(manager.filter_tasks(status="completed"), "COMPLETED TASKS")
            elif f_choice == "2":
                format_task_table(manager.filter_tasks(status="pending"), "PENDING TASKS")
            elif f_choice == "3":
                p = get_input("Priority Level").capitalize()
                format_task_table(manager.filter_tasks(priority=p), f"PRIORITY: {p}")
            elif f_choice == "4":
                c = get_input("Category").capitalize()
                format_task_table(manager.filter_tasks(category=c), f"CATEGORY: {c}")

        elif choice == "8":
            print("\nSort by: 1. Due Date | 2. Priority | 3. Creation Date")
            s_choice = input("Select sort option (1-3): ")
            criteria = { "1": "due_date", "2": "priority", "3": "created_at" }.get(s_choice, "due_date")
            manager.sort_tasks(criteria)
            format_task_table(manager.tasks, f"SORTED BY {criteria.upper()}")

        elif choice == "9":
            stats = manager.get_analytics()
            print(f"\n{Colors.BOLD}{Colors.HEADER}--- ANALYTICS DASHBOARD ---{Colors.ENDC}")
            print(f"Total Tasks:      {stats['total']}")
            print(f"Completed:        {Colors.OKGREEN}{stats['completed']}{Colors.ENDC}")
            print(f"Completion Rate:   {Colors.OKBLUE}{stats['percentage']:.1f}%{Colors.ENDC}")
            print(f"Overdue Tasks:    {Colors.FAIL}{stats['overdue']}{Colors.ENDC}")
            
            # Simple Progress Bar
            bar = "█" * int(stats['percentage'] // 5) + "-" * (20 - int(stats['percentage'] // 5))
            print(f"Progress: [{Colors.OKGREEN}{bar}{Colors.ENDC}]")

        elif choice == "10":
            filename = get_input("Filename to export", default="tasks_export.csv")
            if manager.export_to_csv(filename):
                print_message(f"Data exported to {filename}", "success")
            else:
                print_message("Export failed. Task list might be empty.", "warning")

        elif choice == "11":
            print(f"\n{Colors.OKBLUE}Logging activities and exiting... Goodbye!{Colors.ENDC}")
            sys.exit(0)

        else:
            print_message("Invalid option. Please choose 1-11.", "error")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.FAIL}Application interrupted. Exiting...{Colors.ENDC}")
        sys.exit(1)
