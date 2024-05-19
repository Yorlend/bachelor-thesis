from typing import Annotated
from fastapi import APIRouter, Depends

from api.requests.LocalizationRequest import LocalizationRequest
from api.services.LocalizationService import LocalizationService


LocalizationRouter = APIRouter(
    prefix="/locate",
)


@LocalizationRouter.post("/")
def localize(localizationService: Annotated[LocalizationService, Depends()], request: LocalizationRequest):
    rssi = list[float]
    # calculate rssi
    localizationService.fit()
    return localizationService.localize(rssi)
