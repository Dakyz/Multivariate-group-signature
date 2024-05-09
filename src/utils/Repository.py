from src.utils.Singleton import Singleton
from src.utils.Store import Store


class Repository(metaclass=Singleton):

    def __init__(self):
        self.store = Store()

    def add_user(self, id, sk):
        self.store.add_user(id, sk)

    def update_user_sk(self, id, sk):
        self.store.update_user_sk(id, sk)

    def get_username(self, id):
        return self.store.get_username(id)

    def get_user_emai(self, id):
        return self.store.get_user_email(id)

    def get_user_sk(self, id):
        return self.store.get_user_sk(id)

