
from pydantic import BaseModel

from domain.entities.Fingerprint import FingerprintEntity
from domain.entities.Point2D import Point2D


class CreateFpRequest(BaseModel):
    name: str
    position: tuple[float, float]
    rssi: list[int]

    def toFingerprint(self) -> FingerprintEntity:
        return FingerprintEntity(self.name, Point2D(*self.position), self.rssi)
