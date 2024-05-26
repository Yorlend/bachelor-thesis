
from typing import Annotated

from fastapi import Depends
from api.config.di import ServiceProvider
from domain.entities.Point2D import Point2D
from domain.interactors.FpInteractor import FpInteractor
from domain.optimizers.FpOptimizer import OptimizationStatus


class FpStorageService:
    fpInteractor: FpInteractor

    def __init__(self, fpInteractor: Annotated[FpInteractor, Depends(ServiceProvider.getFpInteractor)]) -> None:
        self.fpInteractor = fpInteractor

    def startOptimization(self, topology: list[Point2D]):
        self.fpInteractor.startOptimization(topology)

    def cancelOptimization(self):
        self.fpInteractor.cancelOptimization()

    def getOptimizationStatus(self) -> OptimizationStatus:
        return self.fpInteractor.getOptimizationStatus()
