from src.components.analyzer import AnalyzeResume
from src.config.configuration import ConfigurationManager

class ResumeAnalyzer:
    def __init__(self):
        pass

    def initiate_resume_analyzing(self):
        try:
            conifig = ConfigurationManager()
            resume_analyzer_config = conifig.get_resume_analyzer_config()
            resume_analyzer = AnalyzeResume(config=resume_analyzer_config)
            resume_analyzer.analyze_resumes()
        except Exception as e:
            raise e