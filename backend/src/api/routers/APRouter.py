
from typing import Annotated
from fastapi import APIRouter, Depends

from api.requests.CreateRouterRequest import CreateRouterRequest
from api.requests.UpdateRouterRequest import UpdateRouterRequest
from api.services.RouterService import RouterService


APRouter = APIRouter(
    prefix="/routers"
)


@APRouter.get("/")
def get(rService: Annotated[RouterService, Depends()]):
    return rService.get()


@APRouter.post("/")
def add(rService: Annotated[RouterService, Depends()], request: CreateRouterRequest):
    rService.add(request.toRouter())


@APRouter.delete("/{name}")
def remove(rService: Annotated[RouterService, Depends()], name: str):
    rService.remove(name)


@APRouter.put("/{name}")
def update(rService: Annotated[RouterService, Depends()], name: str, request: UpdateRouterRequest):
    rService.update(name, request.toRouter(name))
