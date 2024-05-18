
from abc import ABC, abstractmethod

from domain.entities.Fingerprint import FingerprintEntity


class IFpRepository(ABC):
    @abstractmethod
    def get(self) -> list[FingerprintEntity]:
        pass

    @abstractmethod
    def add(self, fingerprint: FingerprintEntity) -> None:
        pass

    @abstractmethod
    def remove(self, name: str) -> None:
        pass

    @abstractmethod
    def update(self, name: str, fingerprint: FingerprintEntity) -> None:
        pass
