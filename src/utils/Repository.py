from src.utils.Singleton import Singleton
from src.utils.store.UserStore import UserStore
from src.utils.store.GroupStore import GroupStore


class Repository(metaclass=Singleton):

    def __init__(self):
        self.user_store = UserStore()
        self.group_store = GroupStore()

    def add_user(self, id, sk):
        self.user_store.add_user(id, sk)

    def update_user_sk(self, id, sk):
        self.user_store.update_user_sk(id, sk)

    def get_username(self, id):
        return self.user_store.get_username(id)

    def get_user_emai(self, id):
        return self.user_store.get_user_email(id)

    def get_user_sk(self, id):
        return self.user_store.get_user_sk(id)

    def update_company_R(self, id, R):
        self.group_store.update_R(id, R)

    def update_company_S(self, id, S):
        self.group_store.update_R(id, S)

    def update_company_g(self, id, g):
        self.group_store.update_R(id, g)

    def get_R(self, id):
        return self.group_store.get_R(id)
    def get_S(self, id):
        return self.group_store.get_S(id)

    def get_g(self, id):
        return self.group_store.get_g(id)

    def add_company(self, id):
        self.group_store.add_company(
            id,
            None,
            None,
            None
        )