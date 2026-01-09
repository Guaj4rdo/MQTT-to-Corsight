import logging
import json
from src.application.ports import FaceRepository
from src.domain.schemas import FaceDetection

logger = logging.getLogger("MockRepository")

class MockFaceRepository(FaceRepository):
    """
    Mock implementation of the FaceRepository for testing and local development.
    Simulates API calls by logging the operations instead of making network requests.
    """
    def create_poi(self, detection: FaceDetection) -> bool:
        """
        Simulates the creation of a POI.

        Args:
            detection (FaceDetection): The detection data.

        Returns:
            bool: Always True (simulated success).
        """
        logger.info("------------------------------------------------")
        logger.info("[LOCAL MODE] SIMULATING CORSIGHT REQUEST")
        logger.info(f"Name: {detection.display_name}")
        logger.info(f"RUT: {detection.rut}")
        logger.info(f"Blacklist: {detection.is_blacklist}")
        logger.info(f"Image length: {len(detection.image_base64)} characters")
        logger.info("Simulated response: 200 OK")
        logger.info("------------------------------------------------")
        return True
