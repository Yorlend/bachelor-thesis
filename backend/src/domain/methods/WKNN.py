from typing import Self
import numpy as np

from numpy import ndarray
from domain.methods.Method import Method


class WKNNMethod(Method):
    def __init__(self, k: int = 3):
        self.k = k

    def fit(self, fp_pos: ndarray, rssi: ndarray):
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
        rssi_dists = rssi_dists[sorted_ids] + 0.001
        weights = (1 / rssi_dists) / np.sum(1 / rssi_dists)
        pos = np.sum(self.fp_pos[sorted_ids] *
                     np.array([weights, weights]).T, axis=0)
        return pos, np.linalg.norm(pos - self.fp_pos[sorted_ids[0]])

    def clone(self) -> Self:
        return WKNNMethod(k=self.k)
