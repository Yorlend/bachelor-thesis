from typing import Annotated
from fastapi import APIRouter, Depends

from api.requests.LocalizationRequest import LocalizationRequest
from api.services.LocalizationService import LocalizationService


LocalizationRouter = APIRouter(
    prefix="/locate",
)


@LocalizationRouter.post("/")
def localize(localizationService: Annotated[LocalizationService, Depends()], request: LocalizationRequest):
    pos, dist = localizationService.localize(
        request.getPosition(), request.topology)
    return {"x": pos.x, "y": pos.y, "closest_x": dist.x, "closest_y": dist.y}
