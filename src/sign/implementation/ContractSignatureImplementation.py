from src.sign.interfaces.ContractSignatureInterface import ContractSignatureInterface
from sage.all import *


class ContractSignatureImplementation(ContractSignatureInterface):

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

    def sign(self, msg, R_2, msk, g_2, S_2):
        # TODO: функция одной компании, получать данные из другой
        t = randint(0, self.P)
        R_1 = pow(t, self.k, self.P)
        # pick R_2?
        R = Zmod(self.P)(R_1 * R_2)
        # TODO: sign out of this world
        g_1 = sign(msk, msg)
        # pick g_2?
        E = self.H(self.to_int(
            self.from_int(self.to_int(self.flatting(g_1)) ^ self.to_int(self.flatting(g_2))) + self.from_int(R)))

        S_1 = Zmod(self.P)(pow(self.X_1, E, self.P) * t)
        # pick S_2?
        S = Zmod(self.P)(S_1 * S_2)
        return (E, S, g_1, g_2)

    def verify(self, msg, big_sign):
        # TODO: учесть что у них разные параметры слать короче их
        if verify(msg, big_sign[2]) != 1 or verify(msg, big_sign[3]) != 1:
            return 0

        R_ = Zmod(P)(pow(big_sign[1], self.k, self.P) * pow(self.Y, -big_sign[0], self.P))
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
        self.Y = pow(self.X_1 * self.X_2, self.k, self.P)
