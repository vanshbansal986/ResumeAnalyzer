from dataclasses import dataclass
from pathlib import Path

@dataclass
class ResumeAnalyzeConfig:
    root_dir: Path
    resume_folder_path: Path
    final_results_file_path: Path
    model_name: str
    system_prompt_path: Path