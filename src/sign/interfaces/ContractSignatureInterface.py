from abc import ABC, abstractmethod

class ContractSignatureInterface(ABC):

    @abstractmethod
    def sign(self):
        pass

    @abstractmethod
    def verify(self):
        pass