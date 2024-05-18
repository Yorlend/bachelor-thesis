
from data.repositories.InMemoryFpRepository import InMemoryFpRepository
from domain.interactors.FpInteractor import FpInteractor
from domain.methods.Gradient import GradientMethod
from domain.methods.Method import Method
from domain.repositories.FpRepository import IFpRepository


class ServiceProvider:
    fpRepository: IFpRepository = InMemoryFpRepository()
    method: Method = GradientMethod()
    fpInteractor: FpInteractor = FpInteractor(fpRepository, method)

    @classmethod
    def getFpInteractor(cls) -> FpInteractor:
        return cls.fpInteractor

    @classmethod
    def getFpRepository(cls) -> IFpRepository:
        return cls.fpRepository

    @classmethod
    def getMethod(cls) -> Method:
        return cls.method
