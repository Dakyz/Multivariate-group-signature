from src.utils.Singleton import Singleton
from src.constants import Constants
from src.sign.implementation.ContractSignatureImplementation import ContractSignatureImplementation


class ContractSchemes(metaclass=Singleton):

    def __init__(self):
        self._contract_schemes = ContractSignatureImplementation()
