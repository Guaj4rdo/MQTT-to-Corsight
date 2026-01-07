from pydantic import BaseModel

# Models for the incoming MQTT message
class Location(BaseModel):
    lat: float
    long: float

class PersonPayload(BaseModel):
    name: str
    rut: str
    blacklist: bool
    image_b64: str

class MqttEvent(BaseModel):
    EventID: str
    loc: Location
    sampleDate: int
    payload: PersonPayload  

# Clean entity for our Use Case
class FaceDetection(BaseModel):
    """
    Clean entity that will use our business logic.
    No longer depends on the exact structure of the MQTT.
    """
    display_name: str
    rut: str
    image_base64: str
    is_blacklist: bool