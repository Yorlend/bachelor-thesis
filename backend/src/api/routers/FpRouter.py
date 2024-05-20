
from typing import Annotated
from fastapi import APIRouter, Depends

from api.requests.CreateFpRequest import CreateFpRequest
from api.requests.TopologyRequest import TopologyRequest
from api.requests.UpdateFpRequest import UpdateFpRequest
from api.services.FpStorageService import FpStorageService


FpRouter = APIRouter(
    prefix="/fingerprints",
)


@FpRouter.get("/")
def get(fpStorageService: Annotated[FpStorageService, Depends()]):
    return fpStorageService.getFingerprints()


@FpRouter.post("/")
def add(fpStorageService: Annotated[FpStorageService, Depends()], request: CreateFpRequest):
    fpStorageService.addFingerprint(request.toFingerprint())


@FpRouter.put("/{name}")
def update(fpStorageService: Annotated[FpStorageService, Depends()], name: str, request: UpdateFpRequest):
    fpStorageService.updateFingerprint(name, request.toFingerprint(name))


@FpRouter.delete("/{name}")
def remove(fpStorageService: Annotated[FpStorageService, Depends()], name: str):
    fpStorageService.removeFingerprint(name)


@FpRouter.post("/optimize")
def optimize(fpStorageService: Annotated[FpStorageService, Depends()], request: TopologyRequest):
    return fpStorageService.optimize(request.toPolygon2D())
