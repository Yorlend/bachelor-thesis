

from domain.entities.Fingerprint import FingerprintEntity
from domain.entities.Point2D import Point2D
from domain.repositories.FpRepository import IFpRepository

fingerprints = list(map(lambda x:
                        FingerprintEntity(
                            f'fp_{x[0]}', Point2D(float(x[1][0]), float(x[1][1])), list(map(int, x[1][2:]))),
                        enumerate(map(lambda x: x.split(","), '''6,2,-37,-58,-68
2,2,-47,-63,-73
2,6,-51,-54,-73
5,6,-53,-52,-74
5,9,-62,-52,-65
1,9,-61,-61,-59
5,12,-55,-39,-74
3,15,-65,-55,-50
6,16,-54,-58,-60
4,17,-61,-72,-68
4,20,-63,-58,-53
6,20,-60,-62,-64
0,20,-82,-69,-57
1,23,-73,-64,-49
4,23,-62,-66,-45
6,23,-68,-67,-54
6,25,-63,-62,-49
3,25,-62,-62,-50
1,26,-73,-66,-66
1,28,-72,-67,-58
3,28,-59,-66,-50
5,30,-61,-64,-48
3,30,-62,-63,-51
0,30,-74,-73,-56'''.split("\n")))))


class InMemoryFpRepository(IFpRepository):
    def __init__(self) -> None:
        self.fingerprints = fingerprints

    def get(self) -> list[FingerprintEntity]:
        return self.fingerprints[:]

    def add(self, fingerprint: FingerprintEntity) -> None:
        self.fingerprints.append(fingerprint)

    def remove(self, name: str) -> None:
        for fingerprint in self.fingerprints:
            if fingerprint.name == name:
                self.fingerprints.remove(fingerprint)
                break

    def update(self, name: str, fingerprint: FingerprintEntity) -> None:
        for i, fp in enumerate(self.fingerprints):
            if fp.name == name:
                self.fingerprints[i] = fingerprint
                break
