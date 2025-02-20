from pathlib import Path
from resource_handler import ResourceHandler
from task_handler import TaskHandler
from argument_handler import ArgumentHandler

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

def handle_command(args):
    command_map = {
        "setup": setup_pytask,
        "config": ResourceHandler.open_config,
        "new": lambda: TaskHandler.create_task(args.new, args.importance, args.message or ""),
        "open": lambda: TaskHandler.open_task(args.open),
        "complete": lambda: TaskHandler.update_task(args.complete, "task_status", "Complete"),
        "delete": lambda: TaskHandler.update_task(args.delete, "task_status", "Deleted"),
        "rename": lambda: handle_rename(args.rename),
        "listtasks": lambda: handle_list_tasks(args),
        "changeenvironment": lambda: ResourceHandler.change_current_environment(args.changeenvironment),
        "changeimportance": lambda: change_importance(args),
        "getenvironment": lambda: handle_get_environment(args),
    }
    
    for key, action in command_map.items():
        if getattr(args, key, None):
            action()
            break

def change_importance(args):
    task = args.changeimportance
    importance = args.importance
    if importance == None:
        print("Missing -i flag, exiting.")
        exit(-1)
    
    TaskHandler.update_task(task, 'task_importance', importance)

def handle_list_tasks(args):
    task_type = args.listtasks # What tasks to retrieve ['current', 'task_id', 'all']
    sort_by = args.sort if args.sort != None else "id" # What to sort by ['id', 'status', 'importance']
    show_completed = args.showcompleted != None
    show_deleted = args.showdeleted != None
    TaskHandler.list_tasks(task_type, sort_by, show_completed, show_deleted)

def handle_get_environment(args):
    if args.getenvironment == "all":
        ResourceHandler.get_all_environments()
    else:
        print(ResourceHandler.get_current_environment())

def handle_rename(args):
    new_name = args[1]
    if not args[0].isnumeric():
        print("Error: You must pass a valid int")
        return
    if not new_name:
        print("Error: Name must be valid")
        return
    task_id = int(args[0])
    TaskHandler.update_task(task_id, "task_name", new_name)


# Main function
def main():
    args = ArgumentHandler.parse_arguments()
    handle_command(args)

main()