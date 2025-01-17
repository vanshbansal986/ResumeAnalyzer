import os
from pathlib import Path
from src.constants import CONFIG_FILE_PATH
from src.utils.common import read_yaml , read_file , create_directories
from src.entity.config_entity import ResumeAnalyzeConfig

class ConfigurationManager:
    def __init__(self , config_file_path = CONFIG_FILE_PATH):
        config = read_yaml(Path(config_file_path))
        self.config = config

        create_directories([self.config.artifacts_root])
    
    def get_resume_analyzer_config(self) -> ResumeAnalyzeConfig:
        config = self.config.resume_analyze
        create_directories([config.root_dir])

        resume_analyzer_config = ResumeAnalyzeConfig(
            root_dir = config.root_dir,
            resume_folder_path = config.resume_folder_path,
            final_results_file_path = config.final_results_file_path,
            model_name = config.model_name,
            system_prompt_path = config.system_prompt_path
        )

        return resume_analyzer_config
