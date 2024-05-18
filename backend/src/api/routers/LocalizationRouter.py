from typing import Annotated
from fastapi import APIRouter, Depends

from api.services.LocalizationService import LocalizationService


LocalizationRouter = APIRouter(
    prefix="/locate",
)


@LocalizationRouter.get("/fit")
def fit(localizationService: Annotated[LocalizationService, Depends()]):
    localizationService.fit()


@LocalizationRouter.post("/")
def localize(localizationService: Annotated[LocalizationService, Depends()], rssi: list[float]):
    return localizationService.localize(rssi)
