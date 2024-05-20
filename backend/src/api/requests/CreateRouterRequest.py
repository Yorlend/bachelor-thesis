

from pydantic import BaseModel

from domain.entities.Point2D import Point2D
from domain.entities.Router import Router


class CreateRouterRequest(BaseModel):
    name: str
    position: tuple[float, float]

    def toRouter(self):
        return Router(self.name, Point2D(self.position))
