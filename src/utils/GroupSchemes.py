from src.utils.Singleton import Singleton
from src.constants import Constants
from src.sign.implementation.GroupSignatureImplementation import GroupSignatureImplementation

class GroupSchemes(metaclass=Singleton):

    def __init__(self):
        self._group_schemes = []
        for _ in range(Constants.COMPANIES_CNT):
            self._group_schemes.append(GroupSignatureImplementation())

    def get_group_scheme(self, group_id: int):
        try:
            return self._group_schemes[group_id]
        except IndexError:
            print(f"self._group_schemes[{group_id}] index error")
