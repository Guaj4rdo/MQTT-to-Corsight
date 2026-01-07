import logging
from src.domain.schemas import FaceDetection
from src.application.ports import FaceRepository

logger = logging.getLogger("UseCase")

class ProcessDetectionUseCase:
    def __init__(self, repository: FaceRepository):
        self.repository = repository

    def execute(self, detection: FaceDetection) -> bool:
        logger.info(f"Processing detection for: {detection.display_name}")
        
        success = self.repository.create_poi(detection)
        
        if success:
            logger.info("✅ Success processing detection")
        else:
            logger.error("❌ Error processing detection")