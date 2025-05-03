import os
import json

class CreateNewAsset:

    def __init__(self, config_path=None):
        if config_path is None:
            # Get the directory of this script
            script_dir = os.path.dirname(__file__)
            # Build path to configs/config.json
            config_path = os.path.join(script_dir, "..", "configs", "config.json")
            config_path = os.path.abspath(config_path)

        with open(config_path, "r") as file:
            config = json.load(file)

        self.project_path = config["project_path"]

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

    def create_new_asset(self, asset_dir_path, department_name, asset_type, asset_name):
        """Check if base path exists; if yes, create subdirectories in one line using create_dir."""
        if not os.path.exists(asset_dir_path): 
            raise FileNotFoundError(f"asset path does not exist, please create project structure: {asset_dir_path}")
        self.create_dir(os.path.join(asset_dir_path, department_name, asset_type), asset_name)
        print(f"Created or confirmed directory: {os.path.join(asset_dir_path, department_name, asset_type, asset_name)}")

    def create_project_structure(self, path, project_name):
        """Creates a new project structure with a base asset directory."""
        project_result = self.create_dir(path, project_name)  # Get the directory info as a dict
        project_path = project_result["path"]  # Extract the 'path' from the result dictionary
        self.create_dir(project_path, "asset")  # Use the 'path' value to create the asset directory



    """
    def initialize_project_dir_structure(self, project_name):
        #Creates the project directory and its subdirectories.
        result = self.create_dir(self.project_path, project_name)
        self.create_dir(result["path"], "asset")
        return result["path"]

    def initialize_department_dir_structure(self, project_name, department_name):
        #Creates a department directory inside the asset folder of a project.
        asset_dir_path = os.path.join(self.project_path, project_name, "asset")
        result = self.create_dir(asset_dir_path, department_name)
        return result["path"]

    def initialize_asset_type_dir_structure(self, project_name, department_name, asset_type):
        #Creates an asset type directory inside the department folder of a project.
        department_dir_path = os.path.join(self.project_path, project_name, "asset", department_name)
        result = self.create_dir(department_dir_path, asset_type)
        return result["path"]

    def initialize_asset_dir_structure(self, project_name, department_name, asset_type, asset_name):
        #Creates an asset directory inside the asset type folder of a department.
        asset_type_dir_path = os.path.join(self.project_path, project_name, "asset", department_name, asset_type)
        result = self.create_dir(asset_type_dir_path, asset_name)
        return result["path"]

    
    
    def initialize_asset_file_type_structure(self, project_name, department_name, asset_type, asset_name, file_format):
        #Creates a format-specific directory (ma, mb, fbx, etc.) inside the asset directory.
        asset_dir_path = os.path.join(self.project_path, project_name, "asset", department_name, asset_type, asset_name)
        result = self.create_dir(asset_dir_path, file_format)
        return result["path"]
    """