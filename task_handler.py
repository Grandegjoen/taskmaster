from resource_handler import ResourceHandler
import subprocess
from rich import print, box
from rich.table import Table

# Define color mappings for statuses
STATUS_COLORS = {
    "Complete": "green",
    "Pending": "yellow",
    "Deleted": "red",
}

# Generate a gradient effect for importance (higher importance = brighter)
IMPORTANCE_GRADIENT = ["dim", "bright_black", "blue", "cyan", "bold magenta"]

class TaskHandler():
    @staticmethod
    def create_task(task_name, task_importance, task_message=""):
        task_name = " ".join(task_name)  # Join the words into a single string
        task_message = " ".join(task_message)  # Join the words into a single string
        db = ResourceHandler.load_db()
        task_id = TaskHandler.get_next_task_id(db)
        task_path = ResourceHandler.get_storage_path() / "tasks" / f"task_{task_id}.md"
        TaskHandler.create_task_file(task_path, task_message)

        environment = ResourceHandler.get_current_environment()
        TaskHandler.save_task_to_db(db, environment, task_name, task_importance, task_path, task_id)
        print(f"Task \"ID: {task_id} - {task_name}\" has been created in the {environment} environment!")

    @staticmethod
    def get_next_task_id(db):
        task_id = 1
        for environment in db:
            task_id += len(db[environment])
        return task_id

    @staticmethod
    def create_task_file(task_path, task_message):
        task_path.parent.mkdir(parents=True, exist_ok=True)
        task_path.touch(exist_ok=True)
        if task_message:
            with task_path.open("w") as f:
                f.write(task_message)

    @staticmethod
    def save_task_to_db(db, environment, task_name, task_importance, task_path, task_id):
        if environment not in db:
            db[environment] = []
        db[environment].append({
            "task_id": task_id,
            "task_name": task_name,
            "task_importance": task_importance or 5,
            "task_path": str(task_path),
            "task_status": "Pending",
        })
        ResourceHandler.save_db(db)

    def update_task(task_id, key, value):
        db = ResourceHandler.load_db()
        for environment, tasks in db.items():
            for task in tasks:
                if task["task_id"] == int(task_id):
                    task[key] = value
                    ResourceHandler.save_db(db)
                    return True
        return False

    
    # Opens task in preferred editor
    def open_task(task_id):
        db = ResourceHandler.load_db()
        editor = ResourceHandler.get_preferred_editor()

        for environment, tasks in db.items():  # Iterate through environments
            for task in tasks:
                if task["task_id"] == task_id:
                    task_path = task["task_path"]
                    print(f"Opening task {task_id} in {environment}: {task_path}")
                    subprocess.run([editor, task_path])  # Open file in preferred editor
                    return

        print(f"No task found with ID {task_id}.")

    def get_filtered_tasks(task_type, show_completed, show_deleted):
        db = ResourceHandler.load_db()
        tasks = []

        if task_type == "current":
            current_env = ResourceHandler.get_current_environment()
            if current_env not in db:
                print("No tasks exist in your current environment")
                return

            for task in db[current_env]:
                if not show_completed and task['task_status'] == "Complete":
                    continue
                if not show_deleted and task['task_status'] == "Deleted":
                    continue

                task_data = {
                    "id": task['task_id'],
                    "name": task['task_name'],
                    "importance": task['task_importance'],
                    "status": task['task_status'],
                    "environment": current_env
                }
                tasks.append(task_data)

        elif task_type == "all":
            for environment in db:
                for task in db[environment]:
                    if not show_completed and task['task_status'] == "Complete":
                        continue
                    if not show_deleted and task['task_status'] == "Deleted":
                        continue
                    task_data = {
                        "id": task['task_id'],
                        "name": task['task_name'],
                        "importance": task['task_importance'],
                        "status": task['task_status'],
                        "environment": environment
                    }
                    tasks.append(task_data)
                    
        elif task_type.isnumeric():
            for environment in db:
                for task in db[environment]:
                    if task['task_id'] == int(task_type):
                        task_data = {
                            "id": task["task_id"],
                            "name": task['task_name'],
                            "importance": task['task_importance'],
                            "status": task['task_status'],
                            "environment": environment
                        }
                        tasks.append(task_data)
        return tasks
    
    def sort_tasks(tasks, sort_by):
        if sort_by == "id":
            return sorted(tasks, key=lambda x: x['id'])
        
        if sort_by == "importance":
            print("Import!")
            return sorted(tasks, key=lambda x: x['importance'], reverse=True)
        
        if sort_by == "status":
            return sorted(tasks, key=lambda x: x['status'])

        print("Invalid sort_by argument given. Exiting.")
        exit(-1)


    def list_tasks(task_type, sort_by, show_completed, show_deleted):
        tasks = TaskHandler.get_filtered_tasks(task_type, show_completed, show_deleted)

        if len(tasks) < 2:
            generate_table(tasks)

        sorted_tasks = TaskHandler.sort_tasks(tasks, sort_by)
        generate_table(sorted_tasks)



def generate_table(tasks):
    caption = "1 Task" if len(tasks) < 2 else ("Tasks: " + str(len(tasks)))
    table = Table(title=caption, box=box.DOUBLE, show_lines=True)
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Task", style="magenta")
    table.add_column("Status", justify="center", style="green")
    table.add_column("Importance", justify="center", style="green")
    table.add_column("Environment", justify="center", style="white")

    for task in tasks:
        status_color = STATUS_COLORS.get(task["status"], "white")
        importance_style = IMPORTANCE_GRADIENT[min(task["importance"] - 1, len(IMPORTANCE_GRADIENT) - 1)]
        table.add_row(
            str(task['id']),
            f"[{status_color}]{task['name']}[/{status_color}]",
            f"[{status_color}]{task['status']}[/{status_color}]",
            f"[{importance_style}]{task['importance']}[/{importance_style}]",
            task['environment']
        )

    print(table)

