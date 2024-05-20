
from pydantic import BaseModel
from api.requests.TopologyRequest import TopologyRequest
from domain.entities.Point2D import Point2D


class LocalizationRequest(BaseModel):
    x: float
    y: float
    topology: TopologyRequest

    def getPosition(self) -> Point2D:
        return Point2D(self.x, self.y)
