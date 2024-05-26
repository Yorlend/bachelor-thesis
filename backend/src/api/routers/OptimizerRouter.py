
from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends

from api.requests.OptimizeRequest import OptimizeRequest
from api.services.FpStorageService import FpStorageService


OptRouter = APIRouter(
    prefix="/optimization",
)


@OptRouter.post("/start")
def optimize(fpStorageService: Annotated[FpStorageService, Depends()], background: BackgroundTasks, request: OptimizeRequest):
    fpStorageService.setOptimizerParams(
        n_iterations=request.n_iterations, n_particles=request.n_particles)
    fpStorageService.optimize(request.topology.toPolygon2D())
    return {"started": True}


@OptRouter.get("/cancel")
def cancel(fpStorageService: Annotated[FpStorageService, Depends()]):
    return fpStorageService.cancel()


@OptRouter.get("/status")
def status(fpStorageService: Annotated[FpStorageService, Depends()]):
    return fpStorageService.getOptimizationStatus()
