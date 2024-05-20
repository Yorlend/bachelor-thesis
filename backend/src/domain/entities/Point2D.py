import numpy as np


class Point2D:
    def __init__(self, x: float | list[float], y: float = None) -> None:
        if y is not None:
            self.x = x
            self.y = y
        else:
            self.x = x[0]
            self.y = x[1]

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __array__(self) -> list[float]:
        return np.array([self.x, self.y])

    def __add__(self, other: 'Point2D') -> 'Point2D':
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point2D') -> 'Point2D':
        return Point2D(self.x - other.x, self.y - other.y)

    def __mul__(self, factor: float) -> 'Point2D':
        return Point2D(self.x * factor, self.y * factor)

    def __rmul__(self, factor: float) -> 'Point2D':
        return Point2D(self.x * factor, self.y * factor)

    def normalized(self) -> 'Point2D':
        length = np.hypot(self.x, self.y)
        return Point2D(self.x / length, self.y / length)

    def rotatedCW90(self) -> 'Point2D':
        return Point2D(-self.y, self.x)

    def rotatedCCW90(self) -> 'Point2D':
        return Point2D(self.y, -self.x)

    def dot(self, other: 'Point2D') -> float:
        return self.x * other.x + self.y * other.y

    @classmethod
    def segments_intersection(cls, p1: 'Point2D', p2: 'Point2D', p3: 'Point2D', p4: 'Point2D') -> tuple[float, float]:
        '''
        Вычисляет коэффициенты u и v пересечения линий, построенных на отрезках (p1, p2) и (p3, p4):

        P1 + u (P2 - P1) = P3 + v (P4 - P3)
        '''

        M = np.array([p1 - p2, p4 - p3])
        d3 = np.array(p1 - p3)
        try:
            uv = d3.dot(np.linalg.inv(M))
            return uv
        except np.linalg.LinAlgError:
            return [np.nan, np.nan]
