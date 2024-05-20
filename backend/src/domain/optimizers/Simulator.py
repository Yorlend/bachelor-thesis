import numpy as np

from domain.entities.Point2D import Point2D
from domain.entities.Polygon2D import Polygon2D


class Simulator:
    @classmethod
    def calculateRssi(cls, router_pos: Point2D, location: Point2D, topology: Polygon2D) -> float:
        # TODO: make use of topology
        delta = location - router_pos
        dist = np.hypot(delta.x, delta.y)
        rssi = -30 * np.log10(dist + 1)
        return rssi

    @classmethod
    def calculateRssiVector(cls, routers: list[Point2D], location: Point2D, topology: Polygon2D) -> list[float]:
        return [cls.calculateRssi(r, location, topology) for r in routers]
