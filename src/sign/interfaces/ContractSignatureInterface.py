from abc import ABC, abstractmethod

class ContractSignatureInterface(ABC):

    @abstractmethod
    def sign(self,  msg, user_id, company_id):
        pass

    @abstractmethod
    def verify(self, msg, big_sign):
        pass