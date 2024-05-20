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
        distances = [[np.inf for j in range(self.test_points_count)] for i in range(self.test_points_count)]
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
        self.distances = distances
        self.points_grad = np.array(self.points_grad)
    

    def predict(self, rssi: np.ndarray) -> tuple[np.ndarray, float]:
        '''
        Функция предсказания позиции агента по уровням сигналов RSSI

        `rssi` - вектор уровней сигналов размерности M, равной числу роутеров в системе

        Возвращает вектор-позицию агента и расстояние до ближайшей опорной точки
        '''

        # выбираем ближайшую опорную точку
        i, pos_closest, rssi_closest = self._get_closest_test_point(rssi)

        # вычисление изменений уровней сигналов от опорной точки по направлениям x y
        P_B = self.points_grad[i].T
        P = rssi - rssi_closest
        offset = np.linalg.inv(P_B.T.dot(P_B)).dot(P_B.T).dot(P)

        # вычисление координат по ближайшей опорной точке
        pos = pos_closest + offset
        return pos, np.linalg.norm(pos - pos_closest)

    def _compute_rssi_grad(self, i: int, distances: np.ndarray) -> np.ndarray:
        closest_idx = np.argsort(distances[i])
        for j, k in itertools.combinations(closest_idx, 2):
            X = np.array([
                self.test_points_pos[j] - self.test_points_pos[i],
                self.test_points_pos[k] - self.test_points_pos[i],
            ])
            if np.linalg.matrix_rank(X.T.dot(X)) == 2:
                Y = np.array([
                    self.test_points_rssi[j] - self.test_points_rssi[i],
                    self.test_points_rssi[k] - self.test_points_rssi[i],
                ])
                break
        else:
            raise ValueError('Cannot compute gradient')
        grad = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)
        return grad

    def _get_closest_test_point(self, rssi: np.ndarray) -> tuple[int, np.ndarray, np.ndarray]:
        D = []
        for i in range(self.test_points_count):
            sum_d = 0
            for j in range(self.routers_count):
                sum_d += np.abs(rssi[j] - self.test_points_rssi[i][j]) ** 2
            D.append(sum_d)
        D = np.array(D)
        # выбираем ближайшего соседа
        idx = np.argsort(D)[0]
        return idx, self.test_points_pos[idx], self.test_points_rssi[idx]
