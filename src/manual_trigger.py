import asyncio
import json
import logging
import sys
from datetime import datetime

# Adjust path to ensure we can import from src
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.infrastructure.config import settings
from src.infrastructure.corsight import CorsightAdapter
from src.infrastructure.mock_repository import MockFaceRepository
from src.application.use_cases import ProcessDetectionUseCase
from src.domain.schemas import MqttEvent, FaceDetection
from src.infrastructure.mqtt import MqttService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ManualTrigger")

import argparse
import base64

def main():
    # 1. Parse Arguments to allow overriding environment and image
    parser = argparse.ArgumentParser(description="Manual Trigger for Corsight Integration")
    parser.add_argument("--prod", action="store_true", help="Force usage of real CorsightAdapter regardless of .env settings")
    parser.add_argument("--image", type=str, help="Path to an image file to use in the payload")
    args = parser.parse_args()

    # Prepare image data
    image_b64 = "base64_placeholder_image_string"
    if args.image:
        try:
            with open(args.image, "rb") as image_file:
                image_b64 = base64.b64encode(image_file.read()).decode('utf-8')
            logger.info(f"Loaded image from {args.image}")
        except Exception as e:
            logger.error(f"Failed to load image: {e}")
            return

    # 2. Sample JSON payload (simulating MQTT message)
    # You can edit this dictionary to test different cases
    sample_payload = {
        "EventID": "test-event-123456",
        "loc": {
            "lat": -33.4569,
            "long": -70.6483
        },
        "sampleDate": int(datetime.now().timestamp() * 1000),
        "payload": {
            "name": "Pedro Pascal",
            "rut": "12.345.678-9",
            "blacklist": True,
            "image_b64": image_b64 
        }
    }

    logger.info("Initializing Manual Trigger...")

    # 3. Select Repository
    # Check if PROD is forced via CLI or set in .env
    if args.prod or settings.ENVIRONMENT != "LOCAL":
        logger.info("Using Real CorsightAdapter (PROD mode)")
        try:
            repository = CorsightAdapter()
        except Exception as e:
            logger.error(f"Failed to initialize CorsightAdapter: {e}")
            return
    else:
        logger.warning("Running in LOCAL mode (Mock Repository). Use --prod to force real CorsightAdapter.")
        repository = MockFaceRepository()

    # 4. Setup Use Case
    use_case = ProcessDetectionUseCase(repository=repository)

    # 5. Simulate the parsing logic from MqttService._on_message
    try:
        # Simulate receiving the json string
        json_str = json.dumps(sample_payload)
        logger.info(f"Simulating incoming MQTT payload: {json_str}")

        raw_data = json.loads(json_str)
        event = MqttEvent(**raw_data)

        detection = FaceDetection(
            display_name=event.payload.name,
            rut=event.payload.rut,
            image_base64=event.payload.image_b64,
            is_blacklist=event.payload.blacklist
        )

        logger.info(f"Parsed Event ID: {event.EventID}, RUT: {detection.rut}")
        
        # 6. Execute Use Case
        use_case.execute(detection)
        
    except Exception as e:
        logger.error(f"Error during manual execution: {e}")

if __name__ == "__main__":
    main()
