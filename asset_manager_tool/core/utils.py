import os
import json
import maya.cmds as cmds
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

    def create_directory(self, dir_path, dir_name):
        """Creates a directory if it doesn't exist. Returns {'created': bool, 'path': str}."""
        full_path = os.path.join(dir_path, dir_name)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"Created directory: {full_path}")
            return {"created": True, "path": full_path}
        else:
            print(f"Directory already exists: {full_path}")
            return {"created": False, "path": full_path}


    def fetch_directories(self, path):
        dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return dirs


    def write_data(self, data, file_path, asset_name, format="json"):
        json_file_path = os.path.join(file_path, f"{asset_name}.{format}")

        if format == "json":
            try:
                # If file exists, load existing data
                if os.path.exists(json_file_path):
                    with open(json_file_path, "r") as file:
                        existing_data = json.load(file)
                    
                    # Merge data → assuming both are dicts
                    if isinstance(existing_data, dict) and isinstance(data, dict):
                        existing_data.update(data)
                    elif isinstance(existing_data, list) and isinstance(data, list):
                        existing_data.extend(data)
                    else:
                        print(f"Incompatible data types: existing is {type(existing_data)}, new is {type(data)}")
                        return
                else:
                    # No existing file → start with new data
                    existing_data = data

                # Write updated data back to the file
                with open(json_file_path, "w") as file:
                    json.dump(existing_data, file, indent=4)
                
                print(f"Data saved to {json_file_path} in JSON format.")
            
            except Exception as e:
                print(f"Error writing data to {json_file_path}: {e}")
                raise
        else:
            print(f"Unsupported format: {format}")

    def save_maya_file(self,file_path, file_name, file_type="mayaAscii"):
        
        
        # Build full file path
        full_file_path = os.path.join(file_path, file_name)
        print(full_file_path)
        # Rename the scene to the desired file path
        cmds.file(rename=full_file_path)
        cmds.file(save=True, type=file_type)

        print(f"Full file path: {full_file_path}")  # Debugging the full file path

        