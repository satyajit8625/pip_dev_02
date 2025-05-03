import os 
import sys
import json
import importlib
from core.utils import FileUtils  # Correct import for FileUtils


class AssetPublishManager:

    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.project_path = self.config.get('project_path')
        self.project_name = self.config.get('project_name')

        if not self.project_path or not self.project_name:
            raise ValueError("Config must include 'project_path' and 'project_name'")
        
        # Full base publish path
        self.asset_dir_path = os.path.join(self.project_path, self.project_name, "asset")

    def load_config(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path, 'r') as f:
            return json.load(f)

    def prepare_publish_folder(self,asset_dir_path,department_name,asset_name,file_type):

        path = os.path.join(self.asset_dir_path,department_name,asset_name)
        FileUtils.create_dir(path,file_type)
        

