

from domain.entities.Point2D import Point2D
from domain.entities.Router import Router
from domain.repositories.RouterRepository import IRouterRepository

routers = [
    Router("router_1", Point2D(0, 0)),
    Router("router_2", Point2D(20, 0)),
    Router("router_3", Point2D(20, 20)),
]


class InMemoryRouterRepository(IRouterRepository):

    def __init__(self) -> None:
        self.routers = routers

    def get(self) -> list[Router]:
        return self.routers[:]

    def add(self, router: Router) -> None:
        self.routers.append(router)

    def remove(self, name: str) -> None:
        for router in self.routers:
            if router.name == name:
                self.routers.remove(router)
                break

    def update(self, name: str, router: Router) -> None:
        for i, r in enumerate(self.routers):
            if r.name == name:
                self.routers[i] = router
                break
