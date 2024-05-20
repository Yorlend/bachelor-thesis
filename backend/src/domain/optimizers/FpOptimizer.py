from abc import ABC, abstractmethod

from domain.entities.Point2D import Point2D
from domain.entities.Polygon2D import Polygon2D
from domain.methods.Method import Method


class FpOptimizer(ABC):
    @abstractmethod
    def optimize(self, method: Method, topology: Polygon2D, routers: list[Point2D]) -> list[Point2D]:
        raise NotImplementedError
