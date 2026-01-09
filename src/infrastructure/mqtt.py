import json
import logging
import paho.mqtt.client as mqtt
from pydantic import ValidationError
from src.infrastructure.config import settings
from src.application.use_cases import ProcessDetectionUseCase
from src.domain.schemas import MqttEvent, FaceDetection

logger = logging.getLogger("MqttService")

class MqttService:
    """
    Service class responsible for handling MQTT connections and messages.
    Subscribes to the configured topic and delegates message processing to the use case.
    """
    def __init__(self, use_case: ProcessDetectionUseCase):
        """
        Initializes the MQTT service.

        Args:
            use_case (ProcessDetectionUseCase): The use case to execute upon receiving a valid event.
        """
        self.client = mqtt.Client()
        self.use_case = use_case
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        """Callback for successful connection."""
        if rc == 0:
            logger.info(f"Connected to MQTT. Subscribed to: {settings.MQTT_TOPIC}")
            client.subscribe(settings.MQTT_TOPIC)
        else:
            logger.error(f"Error connecting to MQTT: {rc}")

    def _on_message(self, client, userdata, msg):
        """Callback for receiving messages."""
        try:
            raw_data = json.loads(msg.payload.decode())
            event = MqttEvent(**raw_data)

            detection = FaceDetection(
                display_name=event.payload.name,
                rut=event.payload.rut,
                image_base64=event.payload.image_b64,
                is_blacklist=event.payload.blacklist
            )
            
            logger.info(f"Event ID: {event.EventID}, RUT: {detection.rut}")

            self.use_case.execute(detection)
            
        except ValidationError as e:
            logger.error(f"Invalid MQTT data: {e}")
        except json.JSONDecodeError:
            logger.error("Payload is not a valid JSON")
        except Exception as e:
            logger.error(f"Error receiving MQTT message: {e}")

    def start(self):
        """Starts the MQTT client loop."""
        if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
        
        self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
        self.client.loop_start()

    def stop(self):
        """Stops the MQTT client loop."""
        self.client.loop_stop()