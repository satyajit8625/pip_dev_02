import os
import json
from core.utils import FileUtils  # Correct import for FileUtils

class CreateNewAsset:
    def __init__(self):
        # Instantiate FileUtils
        self.file_utils = FileUtils()

    def create_new_asset(self, asset_dir_path, department_name, asset_type, asset_name):
        """Check if base path exists; if yes, create subdirectories using FileUtils' create_dir."""
        if not os.path.exists(asset_dir_path):
            raise FileNotFoundError(f"Asset path does not exist, please create project structure: {asset_dir_path}")
        
        # Use FileUtils' create_dir to create the subdirectories
        result = self.file_utils.create_dir(os.path.join(asset_dir_path, department_name, asset_type), asset_name)
        print(f"Created or confirmed directory: {result['path']}")

    def create_project_structure(self, path, project_name):
        """Creates a new project structure with a base asset directory."""
        # Use FileUtils' create_dir to create the project directory
        project_result = self.file_utils.create_dir(path, project_name)
        project_path = project_result["path"]  # Extract the 'path' from the result dictionary
        
        # Use FileUtils' create_dir to create the asset directory inside the project
        self.file_utils.create_dir(project_path, "asset")  
        return project_path


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