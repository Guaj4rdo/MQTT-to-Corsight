import logging
import json
from src.application.ports import FaceRepository
from src.domain.schemas import FaceDetection

logger = logging.getLogger("MockRepository")

class MockFaceRepository(FaceRepository):
    def create_poi(self, detection: FaceDetection) -> bool:
        logger.info("------------------------------------------------")
        logger.info("[LOCAL MODE] SIMULATING CORSIGHT REQUEST")
        logger.info(f"Name: {detection.display_name}")
        logger.info(f"RUT: {detection.rut}")
        logger.info(f"Blacklist: {detection.is_blacklist}")
        logger.info(f"Image length: {len(detection.image_base64)} characters")
        logger.info("✅ Simulated response: 200 OK")
        logger.info("------------------------------------------------")
        return True
