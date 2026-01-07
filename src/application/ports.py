from abc import ABC, abstractmethod
from src.domain.schemas import FaceDetection

class FaceRepository(ABC):
    @abstractmethod
    def create_poi(self, detection: FaceDetection) -> bool:
        pass