
from typing import Annotated

from fastapi import Depends

from api.config.di import ServiceProvider
from domain.entities.Point2D import Point2D
from domain.interactors.FpInteractor import FpInteractor


class LocalizationService:

    def __init__(self, fpInteractor: Annotated[FpInteractor, Depends(ServiceProvider.getFpInteractor)]) -> None:
        self.fpInteractor = fpInteractor

    def localize(self, rssi: list[float]) -> tuple[Point2D, float]:
        return self.fpInteractor.predict(rssi)

    def fit(self):
        self.fpInteractor.fit()
