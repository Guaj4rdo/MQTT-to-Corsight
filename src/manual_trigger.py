import asyncio
import json
import logging
import sys
from datetime import datetime
import os # Added for os.path.exists

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
    parser.add_argument("--url", type=str, help="URL of the simulate endpoint (e.g., http://localhost:8000/simulate)")
    args = parser.parse_args()

    # Logic to load image from file
    # Default to fixtures if exists, otherwise require --image
    DEFAULT_IMAGE_PATH = "tests/fixtures/face.jpg"
    image_path = args.image if args.image else DEFAULT_IMAGE_PATH

    image_b64 = None
    
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as image_file:
                image_b64 = base64.b64encode(image_file.read()).decode('utf-8')
            logger.info(f"Loaded image from {image_path}")
        except Exception as e:
            logger.error(f"Failed to load image: {e}")
            return
    else:
        logger.error(f"Image not found at {image_path}. Please provide a valid image with --image or ensure {DEFAULT_IMAGE_PATH} exists.")
        return

    # 2. Sample JSON payload (simulating MQTT message)
    sample_payload = {
        "EventID": "sim-manual-1",
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

    # 3. Check if we should use HTTP request or Internal Logic
    if args.url:
        import requests
        logger.info(f"Sending simulation request to {args.url}...")
        try:
            # We need to send the MqttEvent structure
            response = requests.post(args.url, json=sample_payload)
            if response.status_code == 200:
                logger.info(f"✅ Simulation Request Sent. Response: {response.json()}")
            else:
                logger.error(f"❌ Failed to send request. Status: {response.status_code}, Body: {response.text}")
        except Exception as e:
            logger.error(f"Exception sending request: {e}")
        return

    logger.info("Initializing Manual Trigger (Internal Mode)...")

    # Internal imports (Delayed to allow script to run as client without dependencies)
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    try:
        from src.infrastructure.config import settings
        from src.infrastructure.corsight import CorsightAdapter
        from src.infrastructure.mock_repository import MockFaceRepository
        from src.application.use_cases import ProcessDetectionUseCase
        from src.domain.schemas import MqttEvent, FaceDetection
    except ImportError as e:
        logger.error(f"Missing dependencies for Internal Mode: {e}")
        logger.error("To use Internal Mode, install requirements.txt. To use Client Mode, provide --url.")
        return

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

    # 5. Simulate the parsing logic
    try:
        json_str = json.dumps(sample_payload)
        logger.info(f"Simulating incoming MQTT payload: {json_str[:100]}...")

        raw_data = json.loads(json_str)
        event = MqttEvent(**raw_data)

        detection = FaceDetection(
            display_name=event.payload.name,
            rut=event.payload.rut,
            image_base64=event.payload.image_b64,
            is_blacklist=event.payload.blacklist
        )

        logger.info(f"Parsed Event ID: {event.EventID}, RUT: {detection.rut}")
        
        use_case.execute(detection)
        
    except Exception as e:
        logger.error(f"Error during manual execution: {e}")

if __name__ == "__main__":
    main()
