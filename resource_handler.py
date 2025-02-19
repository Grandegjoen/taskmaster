from pathlib import Path
import subprocess
import configparser
import json

class ResourceHandler:
    home_dir = Path.home()
    task_dir = home_dir / ".pytask"
    config_file = task_dir / "PyTask.ini"

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
        return {}

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
    
    @classmethod
    def get_current_environment(cls):
        if cls.config_file.exists():
            config = configparser.ConfigParser()
            config.read(cls.config_file)  # Reads the config file
            if "Settings" in config and "current_environment" in config["Settings"]:
                current_environment = config["Settings"]["current_environment"]
                return current_environment
            else:
                return None  # Or a default value
    
    @classmethod
    def get_all_environments(cls):
        db = ResourceHandler.load_db()
        for environment in db:
            print(f"Env: {environment}  | Tasks: {len(db[environment])}.")

    @classmethod
    def change_current_environment(cls, new_env):
        if cls.config_file.exists():
            config = configparser.ConfigParser()
            config.read(cls.config_file)  # Reads the config file
            if "Settings" in config and "current_environment" in config["Settings"]:
                config["Settings"]["current_environment"] = new_env
                with open(cls.config_file, 'w') as configfile:
                    config.write(configfile)