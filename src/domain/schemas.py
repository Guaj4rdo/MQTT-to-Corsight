from pydantic import BaseModel

# Models for the incoming MQTT message
class Location(BaseModel):
    """Geolocation data structure."""
    lat: float
    long: float

class PersonPayload(BaseModel):
    """Details of the person detected in the MQTT payload."""
    name: str
    rut: str
    blacklist: bool
    image_b64: str

class MqttEvent(BaseModel):
    """Structure of the incoming MQTT event."""
    EventID: str
    loc: Location
    sampleDate: int
    payload: PersonPayload  

# Clean entity for our Use Case
class FaceDetection(BaseModel):
    """
    Clean entity used by business logic.
    Decouples the internal domain from the external MQTT message structure.
    """
    display_name: str
    rut: str
    image_base64: str
    is_blacklist: bool