
from abc import ABC, abstractmethod
from typing import Self

from numpy import ndarray


class Method(ABC):

    @abstractmethod
    def fit(self, fp_pos: ndarray, rssi: ndarray) -> None:
        pass

    @abstractmethod
    def predict(self, rssi: ndarray) -> tuple[ndarray, float]:
        pass

    @abstractmethod
    def clone(self) -> Self:
        pass
