from abc import ABC,abstractmethod

class GroupSignature(ABC):

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def sign(self):
        pass

    @abstractmethod
    def verify(self):
        pass

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def join(self):
        pass