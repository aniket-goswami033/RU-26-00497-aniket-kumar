import os
import re
from datetime import datetime

FILE_NAME = "tasks.txt"
PRIORITIES = ["High", "Medium", "Low"]
PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


# ---------------------------------------------------------------- file handling
def load_tasks():
    """Read tasks from the file into a list of dictionaries."""
    tasks = []
    if not os.path.exists(FILE_NAME):
        return tasks
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 5:
                continue
            tasks.append({
                "id": parts[0],
                "title": parts[1],
                "priority": parts[2],
                "due": parts[3],
                "status": parts[4],
            })
    return tasks


def save_tasks(tasks):
    """Write every task back to the file."""
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for t in tasks:
            f.write(f"{t['id']}|{t['title']}|{t['priority']}|{t['due']}|{t['status']}\n")


# -------------------------------------------------------------------- helpers
def format_task(t):
    return f"{t['id']} | {t['title']} | {t['priority']} | {t['due']} | {t['status']}"


def next_task_id(tasks):
    """IDs start from T101 and always increase."""
    numbers = [int(t["id"][1:]) for t in tasks if t["id"][1:].isdigit()]
    return f"T{max(numbers) + 1}" if numbers else "T101"


def valid_priority(text):
    """Return the properly-cased priority, or None if invalid."""
    for p in PRIORITIES:
        if text.strip().lower() == p.lower():
            return p
    return None


def valid_date(text):
    """Accept only real dates written as YYYY-MM-DD."""
    text = text.strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return False
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def pending_count(tasks):
    return sum(1 for t in tasks if t["status"] == "Pending")

def add_task(tasks):
    title = input("Title: ").strip()
    while not title:
        print("Title cannot be empty.")
        title = input("Title: ").strip()

    priority = valid_priority(input("Priority: "))
    while priority is None:
        print("Invalid priority. Enter High, Medium or Low.")
        priority = valid_priority(input("Priority: "))

    due = input("Due: ").strip()
    while not valid_date(due):
        print("Invalid date. Use YYYY-MM-DD.")
        due = input("Due: ").strip()

    task = {
        "id": next_task_id(tasks),
        "title": title,
        "priority": priority,
        "due": due,
        "status": "Pending",
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")
    print(format_task(task))


def view_by_priority(tasks):
    if not tasks:
        print("No tasks found.")
        return
    ordered = sorted(tasks, key=lambda t: (PRIORITY_ORDER.get(t["priority"], 3), t["due"]))
    for t in ordered:
        print(format_task(t))


def show_pending(tasks):
    pending = [t for t in tasks if t["status"] == "Pending"]
    if not pending:
        print("No pending tasks. You are all caught up!")
        return
    for t in pending:
        print(format_task(t))


def complete_task(tasks):
    task_id = input("Task ID: ").strip().upper()
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "Done"
            save_tasks(tasks)
            print(f"Task {task_id} marked as done. Pending tasks: {pending_count(tasks)}")
            return
    print(f"Task {task_id} not found.")


def main():
    tasks = load_tasks()
    while True:
        print("\n--- Daily Task Manager ---")
        print("1. Add")
        print("2. View by priority")
        print("3. Show pending")
        print("4. Complete")
        print("5. Exit")
        try:
            choice = input("Choose an option: ").strip()
        except EOFError:
            break

        try:
            if choice == "1":
                add_task(tasks)
            elif choice == "2":
                view_by_priority(tasks)
            elif choice == "3":
                show_pending(tasks)
            elif choice == "4":
                complete_task(tasks)
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Choose 1-5.")
        except EOFError:
            break


if __name__ == "__main__":
    main()