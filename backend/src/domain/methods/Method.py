
from abc import ABC, abstractmethod

from numpy import ndarray


class Method(ABC):

    @abstractmethod
    def fit(self, fp_pos: ndarray, rssi: ndarray) -> None:
        pass

    @abstractmethod
    def predict(self, rssi: ndarray) -> tuple[ndarray, float]:
        pass
