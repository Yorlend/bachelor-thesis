from typing import Self
import numpy as np

from numpy import ndarray
from domain.methods.Method import Method


class KNNMethod(Method):
    def __init__(self, k: int = 3) -> None:
        self.k = k

    def fit(self, fp_pos: ndarray, rssi: ndarray) -> None:
        self.fp_pos = fp_pos
        self.rssi = rssi
        self.fp_count = rssi.shape[0]
        self.routers_count = rssi.shape[1]

    def predict(self, rssi: ndarray) -> tuple[ndarray, float]:
        rssi_dists = []
        for i in range(self.fp_count):
            sum_d = 0
            for j in range(self.routers_count):
                sum_d += np.abs(rssi[j] - self.rssi[i][j]) ** 2
            rssi_dists.append(sum_d)
        rssi_dists = np.array(rssi_dists)
        # выбираем первые k ближайших соседей
        sorted_ids = np.argsort(rssi_dists)[:self.k]
        # вычисление координат по опорным точкам
        pos = np.sum(self.fp_pos[sorted_ids], axis=0) / self.k
        return pos, np.linalg.norm(pos - self.fp_pos[sorted_ids[0]])

    def clone(self) -> Self:
        return KNNMethod(k=self.k)
