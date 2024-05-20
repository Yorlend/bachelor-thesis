
from typing import Annotated

from fastapi import Depends

from api.config.di import ServiceProvider
from domain.entities.Router import Router
from domain.interactors.RouterInteractor import RouterInteractor


class RouterService:
    rInteractor: RouterInteractor

    def __init__(self, rInteractor: Annotated[RouterInteractor, Depends(ServiceProvider.getRouterInteractor)]) -> None:
        self.rInteractor = rInteractor

    def add(self, router: Router) -> None:
        self.rInteractor.add(router)

    def remove(self, name: str) -> None:
        self.rInteractor.remove(name)

    def update(self, name: str, router: Router) -> None:
        self.rInteractor.update(name, router)

    def get(self) -> list:
        return self.rInteractor.get()
