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
            X = np.array([self.test_points_pos[j] - self.test_points_pos[i], self.test_points_pos[k] - self.test_points_pos[i]])
