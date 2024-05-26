from abc import ABC, abstractmethod

from pydantic import BaseModel

from domain.entities.Point2D import Point2D
from domain.entities.Polygon2D import Polygon2D
from domain.methods.Method import Method


class OptimizationStatus(BaseModel):
    status: str
    progress: float


class FpOptimizer(ABC):
    def setParams(self, **kwargs):
        pass

    @abstractmethod
    def optimize(self, method: Method, topology: Polygon2D, routers: list[Point2D],
                 progress_request=lambda p: None, cancel_request=lambda: False) -> list[Point2D] | None:
        raise NotImplementedError

    @abstractmethod
    def cancel(self):
        raise NotImplementedError

    @abstractmethod
    def status(self) -> OptimizationStatus:
        raise NotImplementedError
