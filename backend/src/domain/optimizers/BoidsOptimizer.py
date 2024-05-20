import numpy as np

from domain.optimizers.FpOptimizer import FpOptimizer
from domain.methods.Method import Method
from domain.entities.Point2D import Point2D
from domain.entities.Polygon2D import Polygon2D
from domain.optimizers.Simulator import Simulator


class Boid:
    def __init__(self, fp_poses: list[Point2D], velocity: list[Point2D], topology: Polygon2D):
        self.fp_poses = fp_poses[:]
        self.velocity = velocity[:]
        self.topology = topology
        self.best_state = fp_poses[:]
        self.best_value = None

    @classmethod
    def random_uniform(cls, topology: Polygon2D, fp_count: int, max_speed: float) -> 'Boid':
        top_left = topology.topLeft()
        bottom_right = topology.bottomRight()
        fp_poses = []
        while len(fp_poses) < fp_count:
            x = np.random.uniform(top_left.x, bottom_right.x)
            y = np.random.uniform(top_left.y, bottom_right.y)
            p = Point2D(x, y)
            if p in topology:
                fp_poses.append(p)
        velocity = [Point2D(np.random.uniform(-max_speed, max_speed, 2))
                    for _ in range(fp_count)]
        return Boid(fp_poses, velocity, topology)

    def evaluate(self, f: callable):
        '''
        Вычислить значение целевой функции для текущей позиции.
        Дополнительно обновить лучшую позицию для данной частицы
        '''

        if self.best_value is None:
            # initial evaluation
            self.best_value = f(self.best_state)
        else:
            curr_value = f(self.fp_poses)
            if curr_value < self.best_value:
                self.best_state = self.fp_poses[:]
                self.best_value = curr_value

    def update_velocity(self, phi_1: float, phi_2: float, global_best_state: list[Point2D], max_velocity_proj: float):
        for i, v in enumerate(self.velocity):
            self.velocity[i] = v + phi_1 * (self.best_state[i] - self.fp_poses[i]) + phi_2 * (
                global_best_state[i] - self.fp_poses[i])
            self.velocity[i].x = np.sign(
                self.velocity[i].x) * min(np.abs(self.velocity[i].x), max_velocity_proj)
            self.velocity[i].y = np.sign(
                self.velocity[i].y) * min(np.abs(self.velocity[i].y), max_velocity_proj)

    def advance(self, dt: float):
        '''
        Продвинуть частицу вдоль направления скорости на величину `dt`.
        Если некоторые точки оказались вне топологии - скорректировать их позицию
        '''

        for i, (p, v) in enumerate(zip(self.fp_poses, self.velocity)):
            new_p, new_v = self.__advance_with_reflect(p, v, dt)
            self.fp_poses[i] = new_p
            self.velocity[i] = new_v

    def __advance_with_reflect(self, p: Point2D, vel: Point2D, dt: float) -> tuple[Point2D, Point2D]:
        new_p = p + vel * dt
        # TODO: replace recursion with a loop
        for edge in self.topology.edges():
            # check segments intersection
            u, v = Point2D.segments_intersection(p, new_p, *edge)
            if 0 <= u <= 1 and 0 <= v <= 1:
                int_p = p + (new_p - p) * u
                n = (edge[1] - edge[0]).rotatedCCW90().normalized()
                # new_p = new_p - n * 2 * n.dot(new_p - int_p)
                vel = vel - n * 2 * n.dot(vel)
                dt_left = (1 - u) * dt
                if dt_left > 1e-3:
                    return self.__advance_with_reflect(int_p, vel, dt_left)
        return new_p, vel


class TravelHistory:
    def __init__(self):
        self.boid_states = []
        self.boid_velocities = []

    def commit(self, boids: list[Boid]):
        self.boid_states.append([boid.fp_poses[:] for boid in boids])
        self.boid_velocities.append([boid.velocity[:] for boid in boids])

    def dump(self, filename_prefix: str):
        np.save(f'{filename_prefix}_pos.npy', np.array(self.boid_states))
        np.save(f'{filename_prefix}_vel.npy', np.array(self.boid_velocities))


class BoidsOptimizer(FpOptimizer):
    TEST_POINT_STEP = 1.0  # meters
    FP_COUNT = 10
    N_BOIDS = 50
    N_ITERATIONS = 50
    MAX_VELOCITY_PROJ = 2.0
    DELTA_TIME = 0.1
    HISTORY_FILENAME_PREFIX = 'opt_history'

    def __init__(self):
        self.method = None
        self.test_points = None
        self.topology = None
        self.routers = None

    def optimize(self, method: Method, topology: Polygon2D, routers: list[Point2D]) -> list[Point2D]:
        self.__initialize(method, topology, routers)
        boids = [Boid.random_uniform(topology, self.__class__.FP_COUNT, self.__class__.MAX_VELOCITY_PROJ)
                 for _ in range(self.__class__.N_BOIDS)]
        # calculate initial values for positions
        for b in boids:
            b.evaluate(self.f)
        history = TravelHistory()
        history.commit(boids)
        # loop until enough
        for iteration in range(self.__class__.N_ITERATIONS):
            global_best_state = boids[0].best_state
            global_best_value = boids[0].best_value
            for b in boids:
                if b.best_value < global_best_value:
                    global_best_value = b.best_value
                    global_best_state = b.best_state
            phi_1 = 0.4 * self.__class__.DELTA_TIME
            phi_2 = 0.6 * self.__class__.DELTA_TIME
            for b in boids:
                # update velocities
                b.update_velocity(phi_1, phi_2, global_best_state,
                                  self.__class__.MAX_VELOCITY_PROJ)
                # advance positions
                b.advance(self.__class__.DELTA_TIME)
                # update values
                b.evaluate(self.f)
            history.commit(boids)
            print('iteration', iteration, 'best value', global_best_value)
        history.dump(self.__class__.HISTORY_FILENAME_PREFIX)
        return global_best_state

    def __initialize(self, method: Method, topology: Polygon2D, routers: list[Point2D]):
        self.method = method
        self.topology = topology
        self.routers = routers
        self.test_points = BoidsOptimizer.__extract_test_points(topology)

    @classmethod
    def __extract_test_points(cls, topology: Polygon2D) -> list[Point2D]:
        half_step = cls.TEST_POINT_STEP / 2
        half_step_vec = Point2D(half_step, half_step)

        top_left = topology.topLeft() + half_step_vec
        bottom_right = topology.bottomRight() - half_step_vec
        delta = bottom_right - top_left

        # TODO: may not work for really small topologies
        x_steps = round(delta.x / cls.TEST_POINT_STEP)
        y_steps = round(delta.y / cls.TEST_POINT_STEP)

        test_points = []
        for y in np.linspace(top_left.y, bottom_right.y, y_steps):
            for x in np.linspace(top_left.x, bottom_right.x, x_steps):
                p = Point2D(x, y)
                if p in topology:
                    test_points.append(p)
        return test_points

    def f(self, fp_poses: list[Point2D]) -> float:
        fp_pos = np.array([(f.x, f.y) for f in fp_poses])
        rssi = np.array([Simulator.calculateRssiVector(
            self.routers, p, self.topology) for p in fp_poses])
        self.method.fit(fp_pos, rssi)
        err = 0
        for p in self.test_points:
            rssi = Simulator.calculateRssiVector(
                self.routers, p, self.topology)
            prediction, _ = self.method.predict(rssi)
            err_vec = Point2D(prediction) - p
            err += np.hypot(err_vec.x, err_vec.y)
        err /= len(self.test_points)
        return err
