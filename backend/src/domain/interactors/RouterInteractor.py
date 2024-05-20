
from domain.entities.Router import Router
from domain.repositories.RouterRepository import IRouterRepository


class RouterInteractor:
    routerRepository: IRouterRepository

    def __init__(self, routerRepository: IRouterRepository) -> None:
        self.routerRepository = routerRepository

    def add(self, router: Router) -> None:
        self.routerRepository.add(router)

    def remove(self, name: str) -> None:
        self.routerRepository.remove(name)

    def update(self, name: str, router: Router) -> None:
        self.routerRepository.update(name, router)

    def get(self) -> list:
        return self.routerRepository.get()
