import time
import numpy as np

from domain.optimizers.FpOptimizer import FpOptimizer, OptimizationStatus
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
            if 0 < u <= 1 and 0 <= v <= 1:
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
    HISTORY_FILENAME_PREFIX = 'opt_history'

    def __init__(self):
        self.method = None
        self.test_points = None
        self.topology = None
        self.routers = None

        # optimizer parameters
        self.n_iterations = 10
        self.n_particles = 50
        self.fp_count = 10
        self.start_poses = None
        self.max_velocity_proj = 2.0
        self.delta_time = 2
        self.test_point_step = 1.0  # meters

        # optimization results
        self.started = False
        self.finished = False
        self.progress = 0
        self.canceled = False
        self.result = None

    def setParams(self, **kwargs):
        if 'n_iterations' in kwargs:
            self.n_iterations = kwargs['n_iterations']
        if 'n_particles' in kwargs:
            self.n_particles = kwargs['n_particles']
        if 'fp_count' in kwargs:
            self.fp_count = kwargs['fp_count']
        if 'start_poses' in kwargs:
            self.start_poses = kwargs['start_poses']
        if 'max_velocity_proj' in kwargs:
            self.max_velocity_proj = kwargs['max_velocity_proj']
        if 'delta_time' in kwargs:
            self.delta_time = kwargs['delta_time']
        if 'test_point_step' in kwargs:
            self.test_point_step = kwargs['test_point_step']

    def optimize(self, method: Method, topology: Polygon2D, routers: list[Point2D]):
        self.started = True
        self.finished = False
        self.canceled = False
        self.progress = 0
        self.result = None
        self.__initialize(method, topology, routers)
        boids = [Boid.random_uniform(topology, self.fp_count, self.max_velocity_proj)
                 for _ in range(self.n_particles)]
        # make use of initial positions
        if self.start_poses is not None:
            boids[0].fp_poses = self.start_poses
        # calculate initial values for positions
        for b in boids:
            b.evaluate(self.f)
        history = TravelHistory()
        history.commit(boids)
        # loop until enough
        for iteration in range(self.n_iterations):
            self.progress = iteration / self.n_iterations
            print('progress:', self.progress)
            if self.canceled:
                break
            global_best_state = boids[0].best_state
            global_best_value = boids[0].best_value
            for b in boids:
                if b.best_value < global_best_value:
                    global_best_value = b.best_value
                    global_best_state = b.best_state
            phi_1 = 0.16 * self.delta_time
            phi_2 = 0.24 * self.delta_time
            for num, b in enumerate(boids):
                self.progress = (
                    iteration + num / self.n_particles) / self.n_iterations
                if self.canceled:
                    break
                # update velocities
                phi_1_rnd = phi_1 * np.random.rand()
                phi_2_rnd = phi_2 * np.random.rand()
                b.update_velocity(phi_1_rnd, phi_2_rnd, global_best_state,
                                  self.max_velocity_proj)
                if self.canceled:
                    break
                # advance positions
                b.advance(self.delta_time)
                if self.canceled:
                    break
                # update values
                b.evaluate(self.f)
            history.commit(boids)
            print('iteration', iteration, 'best value', global_best_value)
        history.dump(self.__class__.HISTORY_FILENAME_PREFIX)
        self.result = None if self.canceled else global_best_state
        self.finished = True
        return self.result

    def cancel(self):
        if self.started:
            self.canceled = True
            while not self.finished:
                time.sleep(0.01)

    def status(self) -> OptimizationStatus:
        if self.canceled:
            return OptimizationStatus(status='canceled', progress=self.progress)
        if self.result is not None:
            return OptimizationStatus(status='done', progress=self.progress)
        if not self.started:
            return OptimizationStatus(status='not_started', progress=self.progress)
        return OptimizationStatus(status='running', progress=self.progress)

    def __initialize(self, method: Method, topology: Polygon2D, routers: list[Point2D]):
        self.method = method
        self.topology = topology
        self.routers = routers
        self.test_points = self.__extract_test_points(topology)

    def __extract_test_points(self, topology: Polygon2D) -> list[Point2D]:
        half_step = self.test_point_step / 2
        half_step_vec = Point2D(half_step, half_step)

        top_left = topology.topLeft() + half_step_vec
        bottom_right = topology.bottomRight() - half_step_vec
        delta = bottom_right - top_left

        # TODO: may not work for really small topologies
        x_steps = round(delta.x / self.test_point_step)
        y_steps = round(delta.y / self.test_point_step)

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
