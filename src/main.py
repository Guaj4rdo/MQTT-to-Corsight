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

# Dependency injection
detection_use_case = ProcessDetectionUseCase(repository=repository)
mqtt_service = MqttService(use_case=detection_use_case)

@asynccontextmanager
async def lifespan(app: FastAPI):
    mqtt_service.start()
    yield
    mqtt_service.stop()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def health():
    return {"status": "ok", "env": os.getenv("ENVIRONMENT")}