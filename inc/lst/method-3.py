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
