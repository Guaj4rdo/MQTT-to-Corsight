from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    ENVIRONMENT: str = "PRODUCTION"
    ENABLE_MQTT: bool = True
    
    MQTT_BROKER: str
    MQTT_PORT: int = 1883
    MQTT_TOPIC: str
    MQTT_USERNAME: str
    MQTT_PASSWORD: str

    CORSIGHT_URL: str
    CORSIGHT_USER: str
    CORSIGHT_PASS: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

