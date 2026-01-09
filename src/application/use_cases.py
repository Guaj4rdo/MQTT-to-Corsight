import logging
from src.domain.schemas import FaceDetection
from src.application.ports import FaceRepository

logger = logging.getLogger("UseCase")

class ProcessDetectionUseCase:
    """
    Use case responsible for processing a face detection event.
    Orchestrates the flow between receiving a detection and persisting it as a POI.
    """
    def __init__(self, repository: FaceRepository):
        """
        Initializes the use case with a repository.

        Args:
            repository (FaceRepository): The interface to the face data storage.
        """
        self.repository = repository

    def execute(self, detection: FaceDetection) -> bool:
        """
        Executes the detection processing logic.

        Args:
            detection (FaceDetection): The detection data to process.

        Returns:
            bool: True if processing was successful, False otherwise.
        """
        logger.info(f"Processing detection for: {detection.display_name}")
        
        success = self.repository.create_poi(detection)
        
        if success:
            logger.info("Success processing detection")
        else:
            logger.error("Error processing detection")
            
        return success