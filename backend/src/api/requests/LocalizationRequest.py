
from domain.entities.Point2D import Point2D


class LocalizationRequest:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def toPoint2D(self) -> Point2D:
        return Point2D(self.x, self.y)
