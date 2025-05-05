import os
import json
from core.utils import FileUtils  # Correct import for FileUtils

class CreateNewAsset:
    def __init__(self):
        # Instantiate FileUtils
        self.file_utils = FileUtils()

    def create_new_asset(self, asset_library_dir_path, department_name, asset_type, asset_name):
        """Check if base path exists; if yes, create subdirectories using FileUtils' create_directory."""
        if not os.path.exists(asset_library_dir_path):
            raise FileNotFoundError(f"Asset path does not exist, please create project structure: {asset_library_dir_path}")
        
        # Use FileUtils' create_directory to create the subdirectories
        result = self.file_utils.create_directory(os.path.join(asset_library_dir_path, department_name, asset_type), asset_name)
        print(f"Created or confirmed directory: {result['path']}")

    def create_project_structure(self, path, project_name):
        """Creates a new project structure with a base asset directory."""
        # Use FileUtils' create_directory to create the project directory
        project_result = self.file_utils.create_directory(path, project_name)
        project_path = project_result["path"]  # Extract the 'path' from the result dictionary
        
        # Use FileUtils' create_directory to create the asset directory inside the project
        self.file_utils.create_directory(project_path, "asset_library")  
        return project_path


    