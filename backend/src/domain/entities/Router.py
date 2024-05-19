
from domain.entities.Point2D import Point2D


class Router:
    def __init__(self, name: str, position: Point2D) -> None:
        self.name = name
        self.position = position

    def __repr__(self) -> str:
        return f"Router(name={self.name}, position={self.position})"
