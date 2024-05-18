
import numpy as np
from domain.entities.Fingerprint import FingerprintEntity
from domain.entities.Point2D import Point2D
from domain.methods.Method import Method
from domain.repositories.FpRepository import IFpRepository


class FpInteractor:
    fpRepository: IFpRepository
    method: Method

    def __init__(self, fpRepository: IFpRepository, method: Method) -> None:
        self.fpRepository = fpRepository
        self.method = method

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

    def predict(self, rssi: list[float]) -> tuple[Point2D, float]:
        rssi = np.array(rssi)

        pos, dist = self.method.predict(rssi)
        return Point2D(pos[0], pos[1]), dist
