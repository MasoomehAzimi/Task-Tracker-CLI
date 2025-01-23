import argparse
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

def update_task(task_id, description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
    print(f"Task with ID {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully.")

def mark_in_progress(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "in-progress"
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as in-progress.")
            return
    print(f"Task with ID {task_id} not found.")

def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as done.")
            return
    print(f"Task with ID {task_id} not found.")

def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task["status"] == status]
    if tasks:
        for task in tasks:
            print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")
    else:
        print("No tasks found.")

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Description of the task")
    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("task_id", type=int, help="ID of the task to update")
    update_parser.add_argument("description", help="New description of the task")
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")
    mark_in_progress_parser = subparsers.add_parser("mark-in-progress", help="Mark a task as in progress")
    mark_in_progress_parser.add_argument("task_id", type=int, help="ID of the task to mark as in progress")
    mark_done_parser = subparsers.add_parser("mark-done", help="Mark a task as done")
    mark_done_parser.add_argument("task_id", type=int, help="ID of the task to mark as done")
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("status", choices=["todo", "in-progress", "done"], nargs="?", help="Filter tasks by status")
    args = parser.parse_args()
    if args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.task_id, args.description)
    elif args.command == "delete":
        delete_task(args.task_id)
    elif args.command == "mark-in-progress":
        mark_in_progress(args.task_id)
    elif args.command == "mark-done":
        mark_done(args.task_id)
    elif args.command == "list":
        list_tasks(args.status)

if __name__ == "__main__":
    main()
