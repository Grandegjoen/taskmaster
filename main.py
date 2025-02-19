import argparse
import subprocess
from pathlib import Path
import json
import configparser

class TaskHandler():
    # If message isn't passed, open the file directly
    def create_task(task_name, task_importance, task_message=""):
        db = ResourceHandler.load_db()
        task_id = 1  # Assign ID based on list 
        for environment in db:
            print(len(db[environment]))
            task_id += len(db[environment])
        task_path = ResourceHandler.get_storage_path() / "tasks" / f"{task_id}.md"
        task_path.parent.mkdir(parents=True, exist_ok=True)

        # Always create the file
        task_path.touch(exist_ok=True)

        environment = "default"

        # Save task content if message exists, otherwise open the task immediately.
        if task_message:
            with task_path.open("w") as f:
                f.write(task_message)
    
        # Ensure environment key exists in database
        if environment not in db:
            db[environment] = []  # Create an empty list for the new environment
        
        # Add to database
        db[environment].append({
            "task_id": task_id,
            "task_name": task_name,
            "task_importance": task_importance,
            "task_path": str(task_path),
            "task_status": "pending",
        })

        ResourceHandler.save_db(db)

        print(f"Task \"ID: {task_id} - {task_name}\" has been created in the {environment} environment!")
        return
        if not task_message:
            TaskHandler.open_task(task_id)
    
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


    # Marks the task as deleted and deletes the corresponding file. Additional flag for deleting it from database maybe?
    def delete_task(task_id):
        db = ResourceHandler.load_db()
        # Search through environments
        for environment, tasks in db.items():
            for task in tasks:
                if task["task_id"] == task_id:
                    task["task_status"] = "deleted"  # Mark as deleted
                    ResourceHandler.save_db(db)
                    print(f"Task {task_id} marked as deleted in environment '{environment}'.")
                    return

        print(f"No task found with ID {task_id}.")


    # Renames the task 
    def rename_task(new_name, task_id):
        db = ResourceHandler.load_db()
        # Search through environments
        for environment, tasks in db.items():
            for task in tasks:
                if task["task_id"] == task_id:
                    task["task_name"] = new_name
                    ResourceHandler.save_db(db)
                    print(f"Task {task_id} renamed to {new_name}.")
                    return

        print(f"No task found with ID {task_id}.")

    # Updates the tasks importance.
    def update_task_importance(task_id, task_importance):
        db = ResourceHandler.load_db()
        # Search through environments
        for environment, tasks in db.items():
            for task in tasks:
                if task["task_id"] == task_id:
                    task["task_importance"] = task_importance
                    ResourceHandler.save_db(db)
                    print(f"Task {task_id} importance updated to {task_importance}.")
                    return
    
    # Marks the task as completed.
    def complete_task(task_id):
        db = ResourceHandler.load_db()
        # Search through environments
        for environment, tasks in db.items():
            for task in tasks:
                if task["task_id"] == task_id:
                    task["status"] = "complete"
                    ResourceHandler.save_db(db)
                    print(f"Task {task_id} is now completed!")
                    return

    # Lists the existising tasks
    def list_tasks():
        db = ResourceHandler.load_db()
        for environment in db:
            for task in environment:
                print(task)

class ArgumentHandler:
    @staticmethod
    def validate_arguments(args):
        return
    
    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Task manager CLI")

        # Mutually exclusive group for main actions
        main_group = parser.add_mutually_exclusive_group()
        main_group.add_argument("-n", "--new", help="Creates a new task. Requires --importance.")
        main_group.add_argument("-o", "--open", type=int, help="Opens a task, given a correct ID.")
        main_group.add_argument("-c", "--complete", help="Marks the specified task ID as complete.")
        main_group.add_argument("-d", "--delete", type=int, help="Deletes the specified task ID.")
        main_group.add_argument("--rename", help="The new name you'd like. Used in conjuction with -id.")

        main_group.add_argument(
            "-lt", "--listtasks",
            nargs="?",  # Allows an optional value
            const="current",
            help="Lists tasks. Use --listtasks <ID> for a specific task or --listtasks all for all tasks."
        )

        main_group.add_argument("-le", "--listenvironment", help="Lists the environments")
        main_group.add_argument("--config", help="Opens the config file in preferred editor. Needs to be done before setup.", action="store_true")
        main_group.add_argument("--setup", help="Initial setup of directories and config", action="store_true")

        # Additional arguments
        parser.add_argument("-m", "--message", help="Message describing the task (used with --new).")
        parser.add_argument("-i", "--importance", type=int, choices=range(1, 11), help="Task importance (1-10).")
        parser.add_argument("-id", type=int, help="Task or environment ID")

        # Parse the arguments
        args = parser.parse_args()

        # Validate arguments
        try:
            ArgumentHandler.validate_arguments(args)
        except ValueError as e:
            print(f"Error: {e}")
            parser.print_help()
            exit(1)

        return args

        
class ResourceHandler:
    home_dir = Path.home()
    task_dir = home_dir / ".pytask"
    config_file = task_dir / "PyTask.ini"
    #task_folder = task_dir / "tasks"
    #db_file = task_dir / "tasks.json"

    @classmethod
    def initial_setup(cls):
        cls.task_dir.mkdir(exist_ok=True)

    @classmethod
    def create_config(cls, storage_path, editor):
        ResourceHandler.initial_setup()
        if not cls.config_file.exists():
            config = configparser.ConfigParser()
            config["Settings"] = {
                "editor": editor,
                "current_environment": "default",
                "storage_path": storage_path
            }

            with cls.config_file.open("w") as f:
                config.write(f)

            print("\n\nConfig file created at", cls.config_file)
            print("\nYou can access it with the -c or --config flag.")

    @classmethod
    def load_db(cls):
        db_file = ResourceHandler.get_storage_path() / "db.json"
        if db_file.exists():
            with db_file.open("r") as f:
                return json.load(f)
        return {"tasks": []}

    @classmethod
    def save_db(cls, db):
        db_file = ResourceHandler.get_storage_path() / "db.json"
        with db_file.open("w") as f:
            json.dump(db, f, indent=4)
    
    @classmethod
    def get_preferred_editor(cls):
        return "vim"
    
    @classmethod
    def open_config(cls):
        editor = ResourceHandler.get_preferred_editor()
        subprocess.run([editor, ResourceHandler.config_file])  # Open file in preferred editor
    
    @classmethod
    def get_storage_path(cls):
        if cls.config_file.exists():
            config = configparser.ConfigParser()
            config.read(cls.config_file)  # Reads the config file
            if "Settings" in config and "storage_path" in config["Settings"]:
                storage_path = Path(config["Settings"]["storage_path"])
                storage_path.mkdir(exist_ok=True)
                return storage_path
            else:
                return None  # Or a default value
            

def setup_pytask():
    storage_path = input("\nWhere would you like to store your data?\nPath: ")
    default_editor = input("\nWhat editor would you like to use? (Leave empty for default system editor)\nEditor: ")
    if not default_editor:
        default_editor = "default"

    path = Path(storage_path)
    if not path.exists():
        print("Invalid path given. Please try again.")
        return

    ResourceHandler.create_config(path, default_editor)
    return
    ResourceHandler.initial_setup()
    ResourceHandler.create_config()

def main():
    args = ArgumentHandler.parse_arguments()

    if args.setup:
        setup_pytask()
        print("Setup complete.")
    elif args.config:
        ResourceHandler.open_config()
    elif args.new:
        TaskHandler.create_task(args.new, args.importance, args.message or "")
    elif args.open:
        TaskHandler.open_task(args.open)
    elif args.complete:
        TaskHandler.complete_task(args.complete)
    elif args.delete:
        TaskHandler.delete_task(args.delete)
    elif args.rename:
        TaskHandler.rename_task(args.rename, args.id)

main()