from os import path
import pickle

from domain.entities.Router import Router
from domain.repositories.RouterRepository import IRouterRepository


class FileRouterRepository(IRouterRepository):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        if path.exists(filename):
            with open(filename, 'rb') as f:
                self.routers = pickle.load(f)
                print(self.routers)
        else:
            self.routers = []

    def _save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.routers, f)

    def get(self) -> list[Router]:
        return self.routers

    def add(self, router: Router) -> None:
        self.routers.append(router)
        self._save()

    def remove(self, name: str) -> None:
        for router in self.routers:
            if router.name == name:
                self.routers.remove(router)
                break
        self._save()

    def update(self, name: str, router: Router) -> None:
        for i, r in enumerate(self.routers):
            if r.name == name:
                self.routers[i] = router
                break
        self._save()
