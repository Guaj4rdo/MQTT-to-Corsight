import httpx
import logging
from src.application.ports import FaceRepository
from src.domain.schemas import FaceDetection
from src.infrastructure.config import settings

logger = logging.getLogger("CorsightAdapter")

class CorsightAdapter(FaceRepository):
    def _get_token(self):
        """
        Método privado para obtener el token de autenticación.
        """
        url = f"{settings.CORSIGHT_URL}/users_service/auth/login/"
        try:
            with httpx.Client(verify=False) as client:
                resp = client.post(url, data={
                    "username": settings.CORSIGHT_USER, 
                    "password": settings.CORSIGHT_PASS
                })
                if resp.status_code == 200:
                    return resp.json()["data"]["access_token"]
                else:
                    logger.error(f"Error login Corsight: {resp.status_code} - {resp.text}")
                    return None
        except Exception as e:
            logger.error(f"Exception connecting to Corsight Auth: {e}")
            return None

    def create_poi(self, detection: FaceDetection) -> bool:
        token = self._get_token()
        if not token:
            logger.error("Failed to get Corsight token. Aborting.")
            return False

        url = f"{settings.CORSIGHT_URL}/poi_service/poi_db/pois/"
        payload = {
            "pois": [{
                "display_name": detection.display_name,
                "poi_notes": {
                    "properties": {
                        "rut": detection.rut,
                        "is_blacklist": detection.is_blacklist,
                        "origin": "mqtt_integration"
                    },
                    "free_notes": f"Importado desde MQTT. RUT: {detection.rut}"
                },
                "face": {
                    "image_payload": {
                        "img": detection.image_base64,
                        "detect": True,
                        "force": True 
                    }
                }
            }]
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            with httpx.Client(verify=False) as client:
                resp = client.post(url, json=payload, headers=headers)
                if resp.status_code == 200:
                    logger.info(f"✅ Success sending to Corsight. Response: {resp.json()}")
                    return True
                
                logger.error(f"❌ Error Corsight {resp.status_code}: {resp.text}")
                return False
        except Exception as e:
            logger.error(f"Exception calling Create POI: {e}")
            return False