
from domain.entities.Point2D import Point2D


class FingerprintEntity:
    name: str
    position: Point2D
    rssi: list[float]

    def __init__(self, name: str, position: Point2D, rssi: list[float]) -> None:
        self.name = name
        self.position = position
        self.rssi = rssi

    def __repr__(self) -> str:
        return f"({self.position}, {self.rssi})"
