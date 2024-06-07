from src.utils.Singleton import Singleton
from src.utils.store.UserStore import UserStore
from src.utils.store.GroupStore import GroupStore


class Repository(metaclass=Singleton):

    def __init__(self):
        self.user_store = UserStore()
        self.group_store = GroupStore()

    def add_user(self, id, sk, pk):
        self.user_store.add_user(id, sk, pk)

    def get_all_pk(self):
        return self.user_store.get_all_pk()

    def update_user_sk(self, id, sk):
        self.user_store.update_user_sk(id, sk)

    def get_username(self, id):
        return self.user_store.get_username(id)

    def get_user_emai(self, id):
        return self.user_store.get_user_email(id)

    def get_user_sk(self, id):
        return self.user_store.get_user_sk(id)

    def get_user_pk(self, id):
        return self.user_store.get_user_pk(id)

    def update_company_R(self, id, R):
        self.group_store.update_R(id, R)

    def update_company_S(self, id, S):
        self.group_store.update_S(id, S)

    def update_company_g(self, id, g):
        self.group_store.update_g(id, g)

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
            None,
            None,
            None
        )

    def get_E(self, id):
        return self.group_store.get_E(id)

    def get_t(self, id):
        return self.group_store.get_t(id)

    def company_update_E(self, id, E):
        self.group_store.update_E(id, E)

    def company_update_t(self, id, t):
        self.group_store.update_t(id, t)