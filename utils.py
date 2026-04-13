import os
from datetime import datetime

# ANSI Color Codes for Professional CLI UX
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_date(date_str):
    """Checks if date is in YYYY-MM-DD format."""
    try:
        if not date_str: return False
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_input(prompt, default=None, validator=None, error_msg="Invalid input."):
    """Gets user input with support for defaults and validation."""
    while True:
        display_prompt = f"{prompt} [{default}]: " if default else f"{prompt}: "
        user_input = input(display_prompt).strip()
        
        if not user_input and default is not None:
            return default
            
        if user_input:
            if validator:
                if validator(user_input):
                    return user_input
                else:
                    print(f"{Colors.FAIL}{error_msg}{Colors.ENDC}")
            else:
                return user_input
        else:
            print(f"{Colors.FAIL}Input cannot be empty.{Colors.ENDC}")

def format_task_table(tasks, title="TASK LIST"):
    """Prints a formatted table of tasks with coloring."""
    if not tasks:
        print(f"\n{Colors.WARNING}No tasks found matching your criteria.{Colors.ENDC}")
        return

    print(f"\n{Colors.HEADER}{Colors.BOLD}--- {title} ---{Colors.ENDC}")
    print(f"{'ID':<4} | {'Status':<6} | {'Title':<25} | {'Priority':<8} | {'Due Date':<11} | {'Category'}")
    print("-" * 80)

    for task in tasks:
        # Determine coloring based on status and deadline
        color = Colors.ENDC
        if task.completed:
            color = Colors.OKGREEN
        elif task.is_overdue():
            color = Colors.FAIL
        elif task.is_due_today():
            color = Colors.WARNING

        status_icon = "DONE" if task.completed else "TODO"
        priority_str = task.priority
        
        # Priority mapping color
        p_color = color
        if not task.completed:
            if task.priority == "High": p_color = Colors.FAIL
            elif task.priority == "Medium": p_color = Colors.WARNING
            elif task.priority == "Low": p_color = Colors.OKCYAN

        row = (f"{color}{task.id:<4}{Colors.ENDC} | "
               f"{color}{status_icon:<6}{Colors.ENDC} | "
               f"{color}{task.title[:25]:<25}{Colors.ENDC} | "
               f"{p_color}{priority_str:<8}{Colors.ENDC} | "
               f"{color}{task.due_date:<11}{Colors.ENDC} | "
               f"{color}{task.category}{Colors.ENDC}")
        print(row)
    print("-" * 80)

def print_message(message, level="info"):
    """Prints a styled message."""
    if level == "info":
        print(f"{Colors.OKBLUE}[INFO]{Colors.ENDC} {message}")
    elif level == "success":
        print(f"{Colors.OKGREEN}[SUCCESS]{Colors.ENDC} {message}")
    elif level == "warning":
        print(f"{Colors.WARNING}[WARNING]{Colors.ENDC} {message}")
    elif level == "error":
        print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} {message}")
