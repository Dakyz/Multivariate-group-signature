from abc import ABC,abstractmethod

class GroupSignatureInterface(ABC):

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def sign(self, msk, msg):
        pass

    @abstractmethod
    def verify(self, msg, sign):
        pass

    @abstractmethod
    def open(self, sign, table):
        pass

    @abstractmethod
    def join(self, id_):
        pass