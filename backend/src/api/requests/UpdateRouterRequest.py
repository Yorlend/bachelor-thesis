

from pydantic import BaseModel

from domain.entities.Point2D import Point2D
from domain.entities.Router import Router


class UpdateRouterRequest(BaseModel):
    position: tuple[float, float]

    def toRouter(self, name: str) -> Router:
        return Router(name, Point2D(self.position))
