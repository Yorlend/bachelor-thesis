import numpy as np
import cProfile

from domain.entities.Fingerprint import FingerprintEntity
from domain.entities.Point2D import Point2D
from domain.entities.Polygon2D import Polygon2D
from domain.methods.Method import Method
from domain.repositories.FpRepository import IFpRepository

from domain.optimizers.FpOptimizer import FpOptimizer, OptimizationStatus
from domain.repositories.RouterRepository import IRouterRepository


class FpInteractor:
    fpRepository: IFpRepository
    rRepository: IRouterRepository
    method: Method
    optimizer: FpOptimizer

    def __init__(self, fpRepository: IFpRepository, rRepository: IRouterRepository, method: Method, optimizer: FpOptimizer) -> None:
        self.rRepository = rRepository
        self.fpRepository = fpRepository
        self.method = method
        self.optimizer = optimizer

    def getFingerprints(self) -> list[FingerprintEntity]:
        return self.fpRepository.get()

    def addFingerprint(self, fingerprint: FingerprintEntity) -> None:
        self.fpRepository.add(fingerprint)

    def removeFingerprint(self, name: str) -> None:
        self.fpRepository.remove(name)

    def updateFingerprint(self, name: str, fingerprint: FingerprintEntity) -> None:
        self.fpRepository.update(name, fingerprint)

    def fit(self):
        fp_pos = np.array([(f.position.x, f.position.y)
                          for f in self.getFingerprints()])
        rssi = np.array([f.rssi for f in self.getFingerprints()])
        self.method.fit(fp_pos, rssi)

    def predict(self, rssi: list[float]) -> tuple[Point2D, Point2D]:
        rssi = np.array(rssi)
        pos, closest = self.method.predict(rssi)
        return Point2D(pos), Point2D(closest)

    def setOptimizerParams(self, **kwargs):
        self.optimizer.setParams(**kwargs)

    def startOptimization(self, topology: Polygon2D) -> list[Point2D]:
        router_pos = [r.position for r in self.rRepository.get()]
        fp_poses = [Point2D(f.position.x, f.position.y)
                    for f in self.getFingerprints()]
        self.optimizer.setParams(
            fp_count=len(self.getFingerprints()),
            start_poses=fp_poses,
        )
        with cProfile.Profile() as pr:
            opt_res = self.optimizer.optimize(
                self.method, topology, router_pos)
            if opt_res is not None:
                pr.dump_stats('profile.prof')
                # update fingerprint positions
                for i in range(len(opt_res)):
                    self.updateFingerprint(
                        self.getFingerprints()[i].name, FingerprintEntity(
                            self.getFingerprints()[i].name, opt_res[i], self.getFingerprints()[i].rssi))

    def cancelOptimization(self):
        self.optimizer.cancel()

    def getOptimizationStatus(self) -> OptimizationStatus:
        return self.optimizer.status()
