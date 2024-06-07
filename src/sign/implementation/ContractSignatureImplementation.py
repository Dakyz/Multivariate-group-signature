from src.sign.interfaces.ContractSignatureInterface import ContractSignatureInterface
from sage.all import *
from src.constants import Constants
from src.utils.GroupSchemes import GroupSchemes
from src.utils.Repository import Repository

low_bound_k = Constants.low_bound_k
low_bound_n = Constants.low_bound_n
up_bound_k = Constants.up_bound_k
up_bound_n = Constants.up_bound_n

class ContractSignatureImplementation(object):

    # [0,1]/SR -> int
    @staticmethod
    def to_int(s):
        return int(''.join(map(str, s)), 2)

    # int -> [0,1]
    @staticmethod
    def from_int(i):
        return list(map(int, list(bin(i)[2:])))

    # [[[0],[1]],[[0],[1]]] -> [0,1]
    @staticmethod
    def flatting(l):  # for multisign
        flat = []
        for i in l:
            if isinstance(i, list) or isinstance(i, tuple):
                flat.extend(ContractSignatureImplementation.flatting(i))
            else:
                flat.append(i)
        return flat

    @staticmethod
    def H(m):
        # TODO: big hash
        return m

    def sign_step1(self, company_id):
        t = randint(0, self.P)
        R_1 = pow(t, self.k, self.P)
        self.repository.company_update_t(company_id, t)
        self.repository.update_company_R(company_id, R_1)

    def sign_step2(self, msg, user_id, company_id):
        company = self.group_schemes.get_group_scheme(company_id)
        msk = self.repository.get_user_sk(user_id)
        # pick R_2?
        # TODO: sign out of this world
        g = company.sign(msk, msg)
        self.repository.update_company_g(company_id, g)

    def sign_step3(self, company_id, other_company_id):

        R_1 = self.repository.get_R(company_id)
        R_2 = self.repository.get_R(other_company_id)
        R = Zmod(self.P)(R_1 * R_2)

        g_1 = self.repository.get_g(company_id)
        g_2 = self.repository.get_g(other_company_id)

        t = self.repository.get_t(company_id)

        print(f"R_1 = {R_1}")
        print(f"R_2 = {R_2}")
        print(f"R = {R}")

        # pick g_2?
        E = self.H(self.to_int(
            self.from_int(self.to_int(self.flatting(g_1)) ^ self.to_int(self.flatting(g_2))) + self.from_int(R)))

        S = Zmod(self.P)(pow(self.X[company_id], E, self.P) * t)

        self.repository.company_update_E(company_id, E)
        self.repository.update_company_S(company_id, S)

    def sign_step4(self, company_id, other_company_id):

        g_1 = self.repository.get_g(company_id)
        g_2 = self.repository.get_g(other_company_id)

        E = self.repository.get_E(company_id)

        # pick S_2?
        S_1 = self.repository.get_S(company_id)
        S_2 = self.repository.get_S(other_company_id)

        S = Zmod(self.P)(S_1 * S_2)
        print("Signed")
        print(f"E = {E}")
        print(f"S = {S}")
        print(f"g_1 = {g_1}")
        print(f"g_2 = {g_2}")
        if company_id < other_company_id:
            return (E, S, g_1, g_2)

        return (E, S, g_2, g_1)


    def verify(self, msg, big_sign):
        # TODO: учесть что у них разные параметры слать короче их

        print(f"k = {self.k}")
        print(f"P = {self.P}")
        print(f"Y = {self.Y}")

        company1 = self.group_schemes.get_group_scheme(0)
        company2 = self.group_schemes.get_group_scheme(1)

        if company1.verify(msg, big_sign[2]) != 1 or company2.verify(msg, big_sign[3]) != 1:
            return 0

        R_ = Zmod(self.P)(pow(big_sign[1], self.k, self.P) * pow(self.Y, -big_sign[0], self.P))
        E_ = self.H(self.to_int(self.from_int(
            self.to_int(self.flatting(big_sign[2])) ^ self.to_int(self.flatting(big_sign[3]))) + self.from_int(R_)))
        if E_ == big_sign[0]:
            return 1
        else:
            return 0

    def __init__(self):
        self.k = next_prime(randint(low_bound_k, up_bound_k))
        self.P = 4
        while not is_prime(self.P):
            self.P = randint(low_bound_n, up_bound_n) * self.k + 1
        self.X_1 = randint(0, self.P)  # первая компания
        self.X_2 = randint(0, self.P)  # вторая компания
        self.X = [self.X_1, self.X_2]
        self.Y = pow(self.X_1 * self.X_2, self.k, self.P)
        print(f"k = {self.k}")
        print(f"P = {self.P}")
        print(f"Y = {self.Y}")
        self.group_schemes = GroupSchemes()
        self.repository = Repository()