
from pydantic import BaseModel

from domain.entities.Fingerprint import FingerprintEntity
from domain.entities.Point2D import Point2D


class UpdateFpRequest(BaseModel):
    position: tuple[float, float]

    def toFingerprint(self, name: str) -> FingerprintEntity:
        return FingerprintEntity(name, Point2D(self.position), [])
