
from typing import Annotated

import numpy as np
from fastapi import Depends

from api.config.di import ServiceProvider
from domain.entities.Point2D import Point2D
from domain.entities.Polygon2D import Polygon2D
from domain.interactors.FpInteractor import FpInteractor
from domain.interactors.RouterInteractor import RouterInteractor
from domain.optimizers.Simulator import Simulator


class LocalizationService:
    fpInteractor: FpInteractor
    rInteractor: RouterInteractor

    def __init__(self, fpInteractor: Annotated[FpInteractor, Depends(ServiceProvider.getFpInteractor)], rInteractor: Annotated[RouterInteractor, Depends(ServiceProvider.getRouterInteractor)]) -> None:
        self.fpInteractor = fpInteractor
        self.rInteractor = rInteractor

    def localize(self, position: Point2D, topology: Polygon2D) -> tuple[Point2D, float]:
        rssi_vec = Simulator.calculateRssiVector(
            [r.position for r in self.rInteractor.get()], position, topology)
        fps = self.fpInteractor.getFingerprints()
        for fp in fps:
            fp.rssi = Simulator.calculateRssiVector(
                [r.position for r in self.rInteractor.get()], fp.position, topology)

        rssi_vec = np.array(rssi_vec)
        self.fit()
        return self.fpInteractor.predict(rssi_vec)

    def fit(self):
        self.fpInteractor.fit()
