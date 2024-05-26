
from data.repositories.FileRouterRepository import FileRouterRepository
from data.repositories.FileFpRepository import FileFpRepository
from data.repositories.InMemoryFpRepository import InMemoryFpRepository
from data.repositories.InMemoryRouterRepository import InMemoryRouterRepository
from domain.interactors.FpInteractor import FpInteractor
from domain.interactors.RouterInteractor import RouterInteractor
from domain.methods.Gradient import GradientMethod
from domain.methods.KNN import KNNMethod
from domain.methods.Method import Method
from domain.methods.WKNN import WKNNMethod
from domain.optimizers.AsyncWrapper import AsyncOptimizerWrapper
from domain.repositories.FpRepository import IFpRepository
from domain.repositories.RouterRepository import IRouterRepository
from domain.optimizers.FpOptimizer import FpOptimizer
from domain.optimizers.BoidsOptimizer import BoidsOptimizer


class ServiceProvider:
    # fpRepository: IFpRepository = InMemoryFpRepository()
    fpRepository: IFpRepository = FileFpRepository('db/data/fingerprints.pkl')
    # rRepository: IRouterRepository = InMemoryRouterRepository()
    rRepository: IRouterRepository = FileRouterRepository(
        'db/data/routers.pkl')

    method: Method = GradientMethod()
    # method: Method = WKNNMethod(k=5)
    optimizer: FpOptimizer = BoidsOptimizer()
    fpInteractor: FpInteractor = FpInteractor(
        fpRepository, rRepository, method, optimizer)
    rInteactor: RouterInteractor = RouterInteractor(rRepository)

    @classmethod
    def getFpInteractor(cls) -> FpInteractor:
        return cls.fpInteractor

    @classmethod
    def getFpRepository(cls) -> IFpRepository:
        return cls.fpRepository

    @classmethod
    def getMethod(cls) -> Method:
        return cls.method

    @classmethod
    def getRouterRepository(cls) -> IRouterRepository:
        return cls.rRepository

    @classmethod
    def getRouterInteractor(cls) -> RouterInteractor:
        return cls.rInteactor
