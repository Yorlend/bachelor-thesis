from abc import ABC, abstractmethod


class IHelloRepository (ABC):
    @abstractmethod
    def sayHello(self):
        pass
