
from pydantic import BaseModel

from domain.entities.Point2D import Point2D
from domain.entities.Polygon2D import Polygon2D


class TopologyRequest(BaseModel):
    vertices: list[tuple[float, float]]

    def toPolygon2D(self) -> Polygon2D:
        return Polygon2D(map(Point2D, self.vertices))
