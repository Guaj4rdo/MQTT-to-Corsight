import asyncio
import json
import logging
import sys
from datetime import datetime

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

    # Valid face image (Person Face) for testing
    # This is a small, valid JPEG of a face to avoid "Added Face contains no faces" error
    DEFAULT_FACE_B64 = "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCADwAPADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWXFlZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU1Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eXqgoOEhYaHiImKkpOUlZaXl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD6pooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAPB/2qv4s+MPhb/wAIr/whupRWX9o/avtPmW0c27y/J243g4xvbp614R/w1V8YP+hms/8AwXwf/E16v+3l/wA09/7iP/trXyt8OfAeufEPxGNF8NRRSXuwyt5sgRVQEAkk/UUAep/8NVfGD/oZrP8A8F8H/wATR/w1V8YP+hms/wDwXwf/ABNc/wDET9nPx/4B0F9Z1e1tLmwjIEslnP5nlZ4BYEA4z3ryagD6V/4aq+MH/QzWf/gvg/8iaP+GqvjB/0M1n/4L4P/AImvIPhn8L/E/wASdRltPC9kswhx508riOKLPTc3r7DJr0Hxl+y38R/Cvh+41ieGwvoLZDJNHZzs8iKBkttZQSB7ZoA6T/hqr4wf9DNZ/wDgvg/+Jo/4aq+MH/QzWf/gvg/+JrwefwvrNv4YtvEU+nyx6LczGCG7bG13GcqO/Y/lWxoPw18V6/4T1DxPpOkSz6HYBjPdb1UDaMtgEgtgcnANAHsH/DVXxg/6Gaz/APBfB/8AE0f8NVfGD/oZrP8A8F8H/wATXyrBdXEt1FHLPI6M4BVmJB5r174/fBOb4RWuhTy66mqHUxKNqwGPZs2+rHOd1AHqX/DVXxg/6Gaz/wDBfB/8TR/w1V8YP+hms/8AwXwf/E18q0UAfVX/AA1V8YP+hms//BfB/wDE0f8ADVXxg/6Gaz/8F8H/AMTXyrRQB9Vf8NVfGD/oZrP/AMF8H/xNH/DVXxg/6Gaz/8F8H/xNfKtFAH1V/wANV8YP+hms/wDwXwf/ABNH/DVXxg/6Gaz/APBfB/8TXyrRQB9Vf8NVfGD/oZrP/wXwf/ABNH/DVXxg/6Gaz/APBfB/8TXyrRQB9Vf8NVfGD/oZrP/wXwf/ABNH/DVXxg/6Gaz/APBfB/8TXyrRQB9Vf8NVfGD/oZrP/wXwf/ABNH/DVXxg/6Gaz/APBfB/8TXyrRQB9Vf8NVfGD/oZrP/wXwf/ABNH/DVXxg/6Gaz/APBfB/8TXyrRQB93fswfHDx98QviZ/ZPinWYbvTvscs3lJZxRneoXByqg9zX1LXwZ+w7/wAlk/7h0/8AOOver6NoAKKKKACiiigAooooAKKKKAPmj9vL/mnv/cR/9ta8C/ZP8ZaT4J+MNnfeIZltrG5gktDO/CwlsFWY9hkYz7177+3l/wA09/7iP/trXyD4L8Kan4z8R2uh6FHHJqFzkRJJIIw2ASRk8ZwKAP0/+JPjnwx4R8G3ereIry0k05omCxllcXORwqj+LPoK/LeTb5jbM7c8Z9K+kNB/ZF+JGqJCt/wD2ZpkKKBtmuvMK/RUBrzn44fB3VvhDqdhZateafe/boy8ctm5IwDg5BAI/KgD6/wD2KbrRpvglZw6UsKXUVxKt8qABjJuJDN65Xbz7V2nxK+MHgv4e6LdXOr6zZyXKowisYJVkmkfBwu0HI+p4r85PB/jzxP4NW6TwvrN3piXQAmFu+3fjOM/TJ/Osy/udV8R6rJdXkt3qWoTnLyOWkkc/wAzQB+hXwK1Dwx8bPgzbaPq1jZ3Elkiw3Nm6AGJwPlkT0yMHI75FeWeP/2idM8F6Zq/gj4W+E7fTbOHzbKW8lUYOfldlQdT1+Zj+FeVfsm+EfG//C1NL1Tw7aXllZ28oF9cTKyQmE/eVs8NnsOeaX9sHwd/wiXxn1KWCPZZasBfQ46ZY/OP++gT+IoA8Yg/4+Y/98fzr7F/b/8A+PLwN/vXX8oq+Oof+PmP/fH86+xf2//APjy8Df7138oqAPjaiivUf2cfhlbfFT4if2NqF3Ja2EFu11cNFjeVUgBVz0ySOe1AHllFfpH/wAMffDL7N5X2O+3Yx5v2tt319P0rxL9oz9lXTfCHhafxN4KuZ3tbQA3VncvvYLn7yt3xnkGgD4/ooooAKKKKACiiigD9Df2F/8AkkF//wBhWT/0XHX0XXzV+whcw/8ACq9StfNT7SupO5iz8wUxpg49ODX0rQAUUUUAFfCn7f3/ACM/hL/r3m/9CWvuuvhT9v7/AJGfwl/17zf+hLQB43+zL/yXjwh/19n/ANAav0rr81P2Zf8AyXjwh/19n/0Bq/SugD6N/Yd/8lk/7h0/846+ja+cv2Hf+Syf9w6f+cdxRt2Y"

    # Prepare image data
    image_b64 = DEFAULT_FACE_B64
    if args.image:
        if os.path.exists(args.image):
            try:
                with open(args.image, "rb") as image_file:
                    image_b64 = base64.b64encode(image_file.read()).decode('utf-8')
                logger.info(f"Loaded image from {args.image}")
            except Exception as e:
                logger.error(f"Failed to load image: {e}")
                return
        else:
            logger.error(f"Image file not found: {args.image}")
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
