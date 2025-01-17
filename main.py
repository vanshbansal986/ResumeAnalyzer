from src.pipeline.analyzer import ResumeAnalyzer
from src import logger

STAGE_NAME = "Resume Analysis Stage"

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ResumeAnalyzer()
        obj.initiate_resume_analyzing()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e