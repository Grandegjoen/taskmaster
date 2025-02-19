import argparse

class ArgumentHandler:
    @staticmethod
    def validate_arguments(args):
        return
    
    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="Task management CLI")
        
        parser = argparse.ArgumentParser(description="Task manager CLI")

        # Mutually exclusive group for main actions
        main_group = parser.add_mutually_exclusive_group()

        main_group.add_argument(
            "-n", "--new",
            nargs="+",
            help="Creates a new task. Requires --importance."
        )

        main_group.add_argument(
            "-o", "--open", 
            type=int, 
            help="Opens a task, given a correct ID."
        )

        main_group.add_argument(
            "-c", "--complete", 
            help="Marks the specified task ID as complete."
        )

        main_group.add_argument(
            "-d", "--delete", 
            type=int, 
            help="Deletes the specified task ID."
        )

        main_group.add_argument(
            "--rename",
            type=str, 
            nargs=2,
            metavar=("ID", "NEW_NAME"),
            help="--rename <task_id> <new_name>."
        )

        main_group.add_argument(
            "-ce", "--changeenvironment", 
            type=str, 
            help="Change to a new environment."
        )

        main_group.add_argument(
            "-lt", "--listtasks",
            nargs="?",
            const="current",
            help="Lists tasks. Use --listtasks <ID> for a specific task or --listtasks all for all tasks."
        )

        main_group.add_argument(
            "-ge", "--getenvironment",
            nargs="?",
            const="current",
            help="Gets the current environment. Add \"all\" to list all available environments."
        )

        main_group.add_argument(
            "--config", 
            help="Opens the config file in preferred editor. Needs to be done before setup.", 
            action="store_true"
        )
        
        main_group.add_argument(
            "--setup", 
            help="Initial setup of directories and config", 
            action="store_true"
        )

        # Additional arguments
        parser.add_argument(
            "-m", "--message", 
            help="Message describing the task (used with --new)."
        )
        
        parser.add_argument(
            "-i", "--importance", 
            type=int, choices=range(1, 11), 
            help="Task importance (1-10)."
        )

        parser.add_argument(
            "-id", 
            type=int, 
            help="Task or environment ID"
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
