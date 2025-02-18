import argparse
import subprocess
from pathlib import Path
import json
import configparser

class TaskHandler():
    # If message isn't passed, open the file directly
    def create_task(task_name, task_importance, task_message=""):
        db = ResourceHandler.load_db()
        task_id = len(db["tasks"]) + 1  # Assign ID based on list length
        task_path = ResourceHandler.task_folder / f"{task_id}.md"

        # Save task content
        with task_path.open("w") as f:
            f.write(task_message)

        # Add to database
        db["tasks"].append({
            "task_id": task_id,
            "task_name": task_name,
            "task_importance": task_importance,
            "task_path": str(task_path),
            "task_status": "pending"
        })

        ResourceHandler.save_db(db)
        print(f"Task \"ID: {task_id} - {task_name}\" created!")
    
    # Opens task in preferred editor
    def open_task(task_id):
        db = ResourceHandler.load_db()
        editor = ResourceHandler.get_preferred_editor()
        try:
            task_path = db['tasks'][task_id - 1]['task_path']
            print(task_path)
            subprocess.run([editor, task_path])  # Pass the task_path as an argument to vim
        except:
            print("There is no task with that ID.")


    # Marks the task as deleted and deletes the corresponding file. Additional flag for deleting it from database maybe?
    def delete_task(task_id):
        pass

    # Renames the task 
    def rename_task(task_id, new_name):
        pass

    # Updates the tasks importance.
    def update_task_importance(task_id, task_importance):
        pass

    # Marks the task as completed.
    def complete_task(task_id):
        pass

    # Lists the existising tasks
    def list_tasks():
        db = ResourceHandler.load_db()
        for task in db["tasks"]:
            print(f"ID: {task['task_id']} - Status: {task['task_status']} - Path: {task['task_path']}")

import argparse

class ArgumentHandler:
    @staticmethod
    def validate_arguments(args):
        if args.new and (not args.importance or not args.open):
            raise ValueError("--new requires --importance (1-10).")

        if args.task_id is None and (args.complete or args.delete or args.rename):
            raise ValueError("--complete, --delete, and --rename require --task_id.")

        if args.rename and not args.message:
            raise ValueError("--rename requires --message to specify the new name.")

        if args.config and (args.new or args.complete or args.delete or args.rename):
            raise ValueError("--config cannot be used with task-related actions.")

        if args.setup and (args.new or args.complete or args.delete or args.rename):
            raise ValueError("--setup should be used alone.")

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Task manager CLI")

        # Mutually exclusive group for main actions
        main_group = parser.add_mutually_exclusive_group()
        main_group.add_argument("-n", "--new", help="Creates a new task. Requires --importance.")
        main_group.add_argument("-o", "--open", type=int, help="Opens a task, given a correct ID.")
        main_group.add_argument("-c", "--complete", help="Marks the specified task ID as complete.")
        main_group.add_argument("-d", "--delete", help="Deletes the specified task ID.")
        main_group.add_argument("-r", "--rename", help="Renames the specified task ID.")
        main_group.add_argument("--config", help="Opens the config file in preferred editor", action="store_true")
        main_group.add_argument("--setup", help="Initial setup of directories and config", action="store_true")

        # Additional arguments
        parser.add_argument("-m", "--message", help="Message describing the task (used with --new).")
        parser.add_argument("-i", "--importance", type=int, choices=range(1, 11), help="Task importance (1-10).")
        parser.add_argument("-id", "--task_id", type=int, help="Task ID")

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
    task_folder = task_dir / "tasks"
    db_file = task_dir / "tasks.json"
    config_file = task_dir / "PyTask.ini"

    @classmethod
    def initial_setup(cls):
        cls.task_dir.mkdir(exist_ok=True)
        cls.task_folder.mkdir(exist_ok=True)

    @classmethod
    def create_config(cls):
        if not cls.config_file.exists():
            config = configparser.ConfigParser()
            config["Settings"] = {
                "editor": "vim" if not Path("C:/Windows").exists() else "notepad"
            }

            with cls.config_file.open("w") as f:
                config.write(f)

            print("Config file created at", cls.config_file)
            print("You can access it with the -c or --config flag.")

    @classmethod
    def load_db(cls):
        if cls.db_file.exists():
            with cls.db_file.open("r") as f:
                return json.load(f)
        return {"tasks": []}

    @classmethod
    def save_db(cls, db):
        with cls.db_file.open("w") as f:
            json.dump(db, f, indent=4)
    
    @classmethod
    def get_preferred_editor(cls):
        return "vim"



def main():
    args = ArgumentHandler.parse_arguments()

    if args.setup:
        ResourceHandler.initial_setup()
        ResourceHandler.create_config()
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
        TaskHandler.rename_task(args.rename)

main()