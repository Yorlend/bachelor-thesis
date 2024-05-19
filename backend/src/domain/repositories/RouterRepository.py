
from abc import ABC, abstractmethod


class IRouterRepository(ABC):
    @abstractmethod
    def get(self) -> list:
        pass

    @abstractmethod
    def add(self, name: str) -> None:
        pass

    @abstractmethod
    def remove(self, name: str) -> None:
        pass

    @abstractmethod
    def update(self, name: str) -> None:
        pass
