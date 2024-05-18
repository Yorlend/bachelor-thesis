
from typing import Annotated

from fastapi import Depends
from api.config.di import ServiceProvider
from domain.entities.Fingerprint import FingerprintEntity
from domain.interactors.FpInteractor import FpInteractor


class FpStorageService:
    fpInteractor: FpInteractor

    def __init__(self, fpInteractor: Annotated[FpInteractor, Depends(ServiceProvider.getFpInteractor)]) -> None:
        self.fpInteractor = fpInteractor

    def addFingerprint(self, fingerprint: FingerprintEntity) -> None:
        self.fpInteractor.addFingerprint(fingerprint)

    def removeFingerprint(self, name: str) -> None:
        self.fpInteractor.removeFingerprint(name)

    def updateFingerprint(self, name: str, fingerprint: FingerprintEntity) -> None:
        self.fpInteractor.updateFingerprint(name, fingerprint)

    def getFingerprints(self) -> list[FingerprintEntity]:
        return self.fpInteractor.getFingerprints()
