import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.infrastructure.config import settings
from src.infrastructure.corsight import CorsightAdapter
from src.infrastructure.mqtt import MqttService
from src.infrastructure.mock_repository import MockFaceRepository
from src.application.use_cases import ProcessDetectionUseCase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

# Dependency selection
if settings.ENVIRONMENT == "LOCAL":
    logger.warning("RUNNING IN LOCAL MODE WITH CORSIGHT MOCK")
    repository = MockFaceRepository()
else:
    logger.info("RUNNING IN PRODUCTION MODE")
    repository = CorsightAdapter()

from src.domain.schemas import MqttEvent, FaceDetection

# Dependency injection
detection_use_case = ProcessDetectionUseCase(repository=repository)
mqtt_service = MqttService(use_case=detection_use_case)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for the FastAPI application.
    Handles startup and shutdown events for the MQTT service.
    """
    logger.info("Starting MQTT to Corsight Adapter v1.1 (Token Fix)")
    if settings.ENABLE_MQTT:
        logger.info("Starting MQTT Service...")
        mqtt_service.start()
    else:
        logger.warning("MQTT Service is DISABLED")
    yield
    if settings.ENABLE_MQTT:
        mqtt_service.stop()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def health():
    """
    Health check endpoint.
    Returns:
        dict: Status, current environment, and MQTT service state.
    """
    return {"status": "ok", "env": os.getenv("ENVIRONMENT"), "mqtt_enabled": settings.ENABLE_MQTT}

@app.post("/simulate")
def simulate_detection(event: MqttEvent):
    """
    Endpoint to manually trigger a detection event without an active MQTT broker.
    Useful for testing and verification purposes.

    Args:
        event (MqttEvent): The simulation payload containing detection details.

    Returns:
        dict: Processing status and success flag.
    """
    logger.info(f"Received manual simulation event: {event.EventID}")
    
    detection = FaceDetection(
        display_name=event.payload.name,
        rut=event.payload.rut,
        image_base64=event.payload.image_b64,
        is_blacklist=event.payload.blacklist
    )
    
    result = detection_use_case.execute(detection)
    return {"status": "processed", "success": result}