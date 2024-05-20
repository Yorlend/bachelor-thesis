from typing import Iterable

from domain.entities.Point2D import Point2D


class Polygon2D:
    def __init__(self, vertices: Iterable[Point2D]):
        self.vertices = tuple(vertices)
        self.__boundary = (
            Point2D(min(p.x for p in self.vertices),
                    min(p.y for p in self.vertices)),
            Point2D(max(p.x for p in self.vertices),
                    max(p.y for p in self.vertices)),
        )

    def topLeft(self) -> Point2D:
        return self.__boundary[0]

    def bottomRight(self) -> Point2D:
        return self.__boundary[1]

    def __contains__(self, p: Point2D) -> bool:
        """
        Checks if a given point `p` is inside the polygon.
        Uses the Winding Number algorithm to determine if a point is inside or outside a polygon.

        The winding number of a point with respect to a polygon is the number of times the polygon's
        boundary curve winds around the point. If the winding number is non-zero, the point is inside the polygon.

        This implementation assumes that the polygon is simple (i.e., it does not self-intersect).
        """
        winding_number = 0
        for i in range(len(self.vertices)):
            v1 = self.vertices[i]
            v2 = self.vertices[(i + 1) % len(self.vertices)]

            if v1.y <= p.y:
                if v2.y > p.y:
                    if self._cross_product(v1, v2, p) > 0:
                        winding_number += 1
            else:
                if v2.y <= p.y:
                    if self._cross_product(v1, v2, p) < 0:
                        winding_number -= 1

        return winding_number != 0

    def _cross_product(self, p1: Point2D, p2: Point2D, p: Point2D) -> float:
        """
        Calculates the cross product of the vectors (p2 - p1) and (p - p1).
        """
        return (p2.x - p1.x) * (p.y - p1.y) - (p2.y - p1.y) * (p.x - p1.x)

    def edges(self) -> Iterable[tuple[Point2D, Point2D]]:
        return zip(self.vertices, [*self.vertices[1:], self.vertices[0]])
