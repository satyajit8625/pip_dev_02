import os
import json

class FileUtils:
    def __init__(self, config_path=None):
        # Initialize with an optional config path, defaulting to a relative path
        if config_path is None:
            # Get the directory of this script
            script_dir = os.path.dirname(__file__)
            # Build path to configs/config.json
            config_path = os.path.join(script_dir, "..", "configs", "config.json")
            config_path = os.path.abspath(config_path)

        # Load the config file
        try:
            with open(config_path, "r") as file:
                config = json.load(file)
            self.project_path = config["project_path"]
        except FileNotFoundError:
            print(f"Config file not found: {config_path}")
            raise
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the config file: {config_path}")
            raise
        except KeyError:
            print(f"Missing 'project_path' in config file: {config_path}")
            raise

    def create_dir(self, dir_path, dir_name):
        """Creates a directory if it doesn't exist. Returns {'created': bool, 'path': str}."""
        full_path = os.path.join(dir_path, dir_name)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"Created directory: {full_path}")
            return {"created": True, "path": full_path}
        else:
            print(f"Directory already exists: {full_path}")
            return {"created": False, "path": full_path}


