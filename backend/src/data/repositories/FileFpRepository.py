from os import path
import pickle

from domain.entities.Fingerprint import FingerprintEntity
from domain.repositories.FpRepository import IFpRepository


class FileFpRepository(IFpRepository):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        if path.exists(filename):
            with open(filename, 'rb') as f:
                self.fingerprints = pickle.load(f)
        else:
            self.fingerprints = []

    def _save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.fingerprints, f)

    def get(self) -> list[FingerprintEntity]:
        return self.fingerprints

    def add(self, fingerprint: FingerprintEntity) -> None:
        self.fingerprints.append(fingerprint)
        self._save()

    def remove(self, name: str) -> None:
        for fingerprint in self.fingerprints:
            if fingerprint.name == name:
                self.fingerprints.remove(fingerprint)
                break
        self._save()

    def update(self, name: str, fingerprint: FingerprintEntity) -> None:
        for i, fp in enumerate(self.fingerprints):
            if fp.name == name:
                self.fingerprints[i] = fingerprint
                break
        self._save()
