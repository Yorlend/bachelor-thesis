from multiprocessing import Process, Value
from domain.entities.Point2D import Point2D
from domain.entities.Polygon2D import Polygon2D
from domain.methods.Method import Method
from domain.optimizers.FpOptimizer import FpOptimizer, OptimizationStatus


class AsyncOptimizerWrapper(FpOptimizer):
    def __init__(self, fpOptimizer: FpOptimizer):
        self.fpOptimizer = fpOptimizer
        self.progress = Value('d', 0)
        self.cancel_flag = Value('b', False)
        self.proc = None

    def optimize(self, method: Method, topology: Polygon2D, routers: list[Point2D]) -> None:
        def worker(progress, cancel_flag):
            def progress_request(v):
                progress.value = v

            def cancel_request():
                return cancel_flag.value
            self.fpOptimizer.optimize(
                method, topology, routers, progress_request=progress_request, cancel_request=cancel_request)
        self.proc = Process(target=worker, args=(
            self.progress, self.cancel_flag))
        self.proc.start()

    def cancel(self):
        self.cancel_flag.value = True
        if self.proc != None:
            self.proc.join()
            self.proc = None

    def status(self) -> OptimizationStatus:
        return OptimizationStatus(status='async', progress=self.progress.value)
