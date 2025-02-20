import argparse
from argparse import RawTextHelpFormatter

class ArgumentHandler:
    @staticmethod
    def validate_arguments(args):
        return
    
    @staticmethod
    def parse_arguments():
        """
        Handles command-line argument parsing for the Task Management CLI.

        Main Actions (Mutually Exclusive):
        - `--new <task_name>`: Creates a new task. MESSAGE and IMPORTANCE are optional arguments here.
        - `--open <task_id>`: Opens an existing task by ID.
        - `--complete <task_id>`: Marks a task as complete.
        - `--delete <task_id>`: Deletes a task.
        - `--rename <task_id> <new_name>`: Renames a task.
        - `--changeenvironment <env_name>`: Switches to a different environment.
        - `--listtasks [task_id|all]`: Lists tasks. Defaults to the current environment if no argument is given.
        - `--getenvironment [current|all]`: Retrieves the current environment or lists all available ones.
        - `--config`: Opens the configuration file in the preferred editor.
        - `--setup`: Performs initial setup of directories and config.

        Additional Arguments:
        - `--message <text>`: A description for a new task (used with `--new`).
        - `--importance <1-10>`: Sets a task's importance level (1-10).
        - `--id <task_id>`: Specifies a task or environment ID (used with various actions).
        """
        parser = argparse.ArgumentParser(
            description="Task Management CLI",
            epilog="For more help, run `task --help`.",
            formatter_class=RawTextHelpFormatter
        )
        # Mutually exclusive group for main actions
        main_group = parser.add_mutually_exclusive_group()

        main_group.add_argument(
            "-n", "--new",
            nargs="+",
            metavar="My Task",
            help="Creates a new task.\n\nOptional arguments:\n-m/--message <your message>\n-i/--importance <1-10>.\nExample: <task --new Buy computers -m Remember to buy the computers by end of week -i 8>\n\n"
        )

        main_group.add_argument(
            "-o", "--open",
            metavar="3",
            type=int, 
            help="Opens an existing task by ID. No arguments required.\nExample: <task -o 3>\n\n"
        )

        main_group.add_argument(
            "-c", "--complete", 
            help="Completes an existing task by ID. No arguments required.\nExample: <task -c 3>\n\n"
        )

        main_group.add_argument(
            "-d", "--delete", 
            type=int, 
            help="Deletes an existing task by ID. No arguments required.\nDoes not delete the file itself, but rather marks it as deleted.\nExample: <task -d 3>\n\n"
        )

        main_group.add_argument(
            "--rename",
            type=str, 
            nargs=2,
            metavar=("ID", "NEW_NAME"),
            help="Renames an existing task.\nExample: <task --rename 4 \"New name\"\n\n"
        )

        main_group.add_argument(
            "-ce", "--changeenvironment", 
            type=str, 
            help="Changes the environment / task category, creating a new one if it doesn't already exist.\nExample: <task -ce new_environment>\n\n"
        )

        main_group.add_argument(
            "-lt", "--listtasks",
            nargs="?",
            const="current",
            help="[<task_id>|current(default)|all]: \nExample 1: <task -lt 4> | Displays data on task with ID 4.\nExample 2: <task -lt all> | Displays all tasks.\nExample 3: <task -lt> | Lists tasks in current environment.\n\n"
        )

        main_group.add_argument(
            "-ge", "--getenvironment",
            nargs="?",
            const="current",
            help="[current|all]: \nExample 1: <task -ge> | Defaults to current, printing your current environment.\nExample 2: <task -ge all> | Lists all your environments.\n\n"
        )

        main_group.add_argument(
            "--config", 
            help="Opens the configuration file in the preferred editor.\n\n", 
            action="store_true"
        )
        
        main_group.add_argument(
            "--setup", 
            help="Performs initial setup of directories and config.\n\n", 
            action="store_true"
        )

        # Additional arguments
        parser.add_argument(
            "-m", "--message",
            nargs="+",
        )
        
        parser.add_argument(
            "-i", "--importance",
            type=int, 
            choices=range(1, 11), 
        )

        parser.add_argument(
            "-s", "--sort",
            const="id",
            help="[id(default)|importance|status]",
            choices=['id', 'importance', 'status'],
            nargs="?",
        )

        parser.add_argument(
            "--showcompleted",
            const=False,
            type=bool,
            help="Include this flag to include completed tasks in -lt",
            nargs="?",
        )

        parser.add_argument(
            "--showdeleted",
            const=False,
            type=bool,
            help="Include this flag to include deleted tasks in -lt",
            nargs="?",
        )

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
