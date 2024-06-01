import numpy as np
import itertools


class Model:
    def fit(self, test_points_pos: np.ndarray, test_points_rssi: np.ndarray):
        '''
        Функция обучения модели

        `test_points_pos` - матрица позиций Nx2 опорных точек
        `test_points_rssi` - матрица уровней сигналов NxM от M роутеров для каждой опорной точки
        '''

        self.test_points_pos = test_points_pos
        self.test_points_rssi = test_points_rssi
        self.test_points_count = test_points_rssi.shape[0]
        self.routers_count = test_points_rssi.shape[1]

        # Подготовительный этап - вычисление матрицы расстояний между опорными точками
        distances = [[np.inf for j in range(self.test_points_count)] for i in range(
            self.test_points_count)]
        for i, (xi, yi) in enumerate(self.test_points_pos[:-1]):
            for j, (xj, yj) in enumerate(self.test_points_pos[i+1:]):
                d = np.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)
                distances[i][i+1+j] = d
                distances[i+1+j][i] = d

        # Вычисление градиентов в каждой опорной точке
        self.points_grad = []
        for i in range(self.test_points_count):
            # Вычислить градиент в точке i
            grad = self._compute_rssi_grad(i, distances)
            self.points_grad.append(grad)
