from src.sign.interfaces.GroupSignatureInterface import GroupSignatureInterface
from sage.all import *
from sympy import symbols, Poly
from collections import Counter
from src.utils.Repository import Repository

class GroupSignatureImplementation(GroupSignatureInterface):

    # GF -> len -> [rand_elem_GF]
    @staticmethod
    def new_row(field, count):
        while 1:
            row = []
            elements_sum = 0
            for i in range(count):
                row.append(field.random_element())
                elements_sum += row[-1]
            if elements_sum == 0:
                continue
            else:
                break
        return row

    # SR -> [0,1]
    @staticmethod
    def from_poly(poly, size):
        if poly == 1:
            return [0] * (size - 1) + [1]
        elif poly == 0:
            return [0] * size
        else:
            return [0] * (size - len(Poly(poly).all_coeffs())) + Poly(poly).all_coeffs()

    # [0,1] -> SR
    @staticmethod
    def to_poly(poly):
        new = SR(0)
        poly.reverse()
        for i in range(len(poly)):
            new += poly[i] * x ** i
        poly.reverse()
        return GF(q ** len(poly), 'x')(str(new))

    # [0,1]/SR -> int
    @staticmethod
    def to_int(poly, size, s):
        if s == 0:
            s = GroupSignatureImplementation.from_poly(poly, size)
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
                flat.extend(GroupSignatureImplementation.flatting(i))
            else:
                flat.append(i)
        return flat

    @staticmethod
    def mapping(size, fn, elem):
        nums = GroupSignatureImplementation.from_poly(elem, size)
        new = []
        for i in range(size):
            tmp = 0
            for j in range(size):
                tmp += GF(q)(nums[j]) * GF(q)(fn[i][j])
            new.append(ZZ(GF(q)(tmp)))
        return new

    def S(self, elem):  # m -> m
        return self.to_poly(self.mapping(m, self.S_matrix, elem))

    def T(self, elem):  # n -> n
        return self.to_poly(self.mapping(n, self.T_matrix, elem))

    def F(self, elem):  # central map n -> m
        nums = self.from_poly(elem, n)
        new = []
        for i in range(m):
            tmp = 0
            for j in range(n):
                tmp += GF(q)(nums[j]) * GF(q)(self.F_matrix[i][j])
            new.append(ZZ(GF(q)(tmp)))
        return self.to_poly(new)

    def S_(self, elem):  # m -> m
        return self.to_poly(self.mapping(m, self.S_inv, elem))

    def T_(self, elem):  # n -> n
        return self.to_poly(self.mapping(n, self.T_inv, elem))

    def F_(self, elem, mode):  # central map n <- m
        v = self.F_matrix.solve_right(vector(GF(q), self.from_poly(elem, m)))
        res = list(map(ZZ, list(v)))
        if mode == 1:
            res = self.from_poly(self.to_poly(self.from_int(self.to_int(0,1,res)^self.F_helper)), n)
        return self.to_poly(res)

    def R(self, elem):  # m -> m
        return self.to_poly(self.mapping(m, self.R_matrix, elem))

    @staticmethod
    def H(elem):  # [0,1]**n -> [0,1]**n
        # TODO: hash44
        new = (elem * 3 + 12) % 2 ** (n + 1)
        return [0] * (n - len(bin(new)[2:])) + GroupSignatureImplementation.from_int(new)

    def P(self, elem):  # S x F x T n -> m
        return self.S(self.F(self.T(elem)))

    def P_(self, elem, mode):  # opposite m -> n
        return self.T_(self.F_(self.S_(elem), mode))

    def P__(self, elem):  # P + R
        return GF(q ** m, 'x')(str(SR(str(self.P(self.to_poly(self.from_poly(elem, n + m)[:n])))
                                      + ' + ' + str(self.R(self.to_poly(self.from_poly(elem, n + m)[-m:])))).expand()))

    def linear_map(self, a, b):
        return self.P__(a + b) - self.P__(a) - self.P__(b) + self.P__(0)

    def setup(self):
        k = GF(q ** m, 'x').random_element()
        while 1:
            try:
                self.S_matrix = Matrix(GF(q, 'x'), [self.new_row(GF(q, 'x'), m) for i in range(m)])
                self.S_inv = self.S_matrix.inverse()
                break
            except:
                continue
        while 1:
            try:
                self.T_matrix = Matrix(GF(q, 'x'), [self.new_row(GF(q, 'x'), n) for i in range(n)])
                self.T_inv = self.T_matrix.inverse()
                break
            except:
                continue
        while 1:
            try:
                self.R_matrix = Matrix(GF(q, 'x'), [self.new_row(GF(q, 'x'), m) for i in range(m)])
                self.R_matrix.inverse()
                break
            except:
                continue

        while 1:
            try:
                self.F_matrix = Matrix(GF(q, 'x'), [self.new_row(GF(q, 'x'), n) for i in range(m)])
                [self.F_matrix.solve_right(vector(GF(q), (self.from_poly(self.to_poly(self.from_int(i)), m)))) for i in
                 range(q ** m)]
                break
            except:
                continue
        for i in range(1, 2 ** n):
            lin = list(map(ZZ, list(self.F_matrix * vector(GF(q), self.from_poly(self.to_poly(self.from_int(i)), n)))))
            if self.to_int(0, 1, lin) == 0:
                self.F_helper = i
                break
        # TODO: join method another blin
        # join(1)
        # join(2)
        # join(3)
        self.rep = Repository()

        # return 0

    def sign(self, msk, msg):
        # TODO: hash1
        M = msg  # H_1(to_int(0,1,from_poly(P(x), m) + from_int(msg)))
        # step 1
        r = []
        t = []
        g = []
        e = []
        c = []
        COMIT = []
        Resp_0 = []
        for i in range(rounds):
            ri = []
            ti = []
            gi = []
            ei = []
            ri.append(GF(q ** (n + m), 'x').random_element())
            ti.append(GF(q ** (n + m), 'x').random_element())
            gi.append(GF(q ** (n + m), 'x').random_element())
            gi.append(GF(q ** (n + m), 'x').random_element())
            ei.append(GF(q ** m, 'x').random_element())
            ri.append(GF(q ** (n + m), 'x')(str(msk)) - ri[0])
            c.append((self.from_poly(ri[0], n + m), self.from_poly(ti[0], n + m),
                      self.from_poly(ei[0], m), self.from_poly(gi[0], n + m)))
            c.append((self.from_poly(ri[1], n + m), self.from_poly(self.linear_map(ti[0], ri[1]) + ei[0], m),
                      self.from_poly(gi[1], n + m)))
            COMIT += [(c[i * 2], c[i * 2 + 1])]
            del10 = self.to_poly(self.from_poly(ri[0], n + m)[:n])
            del11 = self.to_poly(self.from_poly(ri[1], n + m)[:n])
            del20 = self.to_poly(self.from_poly(gi[0], n + m)[:n])
            del21 = self.to_poly(self.from_poly(gi[1], n + m)[:n])
            Resp_0 += [(self.from_poly(self.P(del10 + del20), n), self.from_poly(self.P(del20), n),
                        self.from_poly(self.P(del11 + del21), n), self.from_poly(self.P(del21), n),
                        self.H(self.to_int(del10 + del20, n, 0)), self.H(self.to_int(del20, n, 0)),
                        self.H(self.to_int(del11 + del21, n, 0)), self.H(self.to_int(del21, n, 0)))]
            r += [ri]
            t += [ti]
            g += [gi]
            e += [ei]

        # step 2
        a = 1  # H_2(to_int(0,1,from_int(M)+flatting(COMIT)+flatting(Resp_0)))
        # TODO: hash2

        Resp_1 = []
        for i in range(rounds):
            # step 3
            t[i].append(GF(q ** (n + m), 'x')(a * r[i][0] - t[i][0]))
            e[i].append(GF(q ** m, 'x')(a * self.P__(r[i][0]) - e[i][0]))  ###

            # step 4
            Resp_1 += [(self.from_poly(t[i][1], n + m), self.from_poly(e[i][1], m))]

        # step 5
        # TODO hash3
        chl = 1  # 0 #H_3(to_int(0,1,from_int(M)+flatting(COMIT)+flatting(Resp_0)+flatting(Resp_1))) # 0 or 1

        Resp_2 = []
        for i in range(rounds):
            # step 6
            Resp_2 += [(self.from_poly(r[i][chl], n + m), self.from_poly(g[i][chl], n + m))]

        # step 7
        return (COMIT, Resp_0, Resp_1, Resp_2)

    def verify(self, msg, sign):
        # step 1
        # TODO: hashs again
        M = msg  # H_1(to_int(0,1,from_poly(P(x), m) + from_int(msg)))
        a = 1  # H_2(to_int(0,1,from_int(M)+flatting(sign[0])+flatting(sign[1])))
        chl = 1  # 0#H_3(to_int(0,1,from_int(M)+flatting(sign[0])+flatting(sign[1])+flatting(sign[2])))

        # step 2
        # parsing

        for i in range(rounds):
            # step 3
            gam1 = self.to_poly((sign[3][i][0])[:n])
            gam2 = self.to_poly((sign[3][i][1])[:n])
            if chl == 0:
                if sign[0][i][0] != (sign[3][i][0], self.from_poly(
                        GF(q ** (n + m), 'x')(a * self.to_poly(sign[3][i][0]) - self.to_poly(sign[2][i][0])), n + m),
                                     self.from_poly(
                                             a * self.P__(self.to_poly(sign[3][i][0])) - self.to_poly(sign[2][i][1]),
                                             m), sign[3][i][1]):
                    return 0
                if self.from_poly(self.P(gam1 + gam2), n) != sign[1][i][0] or self.from_poly(self.P(gam2), n) != \
                        sign[1][i][1] or self.H(self.to_int(gam1 + gam2, n, 0)) != sign[1][i][4] or self.H(
                        self.to_int(gam2, n, 0)) != sign[1][i][5]:
                    return 0
            elif chl == 1:
                if sign[0][i][1] != (sign[3][i][0], self.from_poly(
                        a * (self.k - self.P__(self.to_poly(sign[3][i][0])) + self.P__(0)) - self.linear_map(
                                self.to_poly(sign[2][i][0]), self.to_poly(sign[3][i][0])) - self.to_poly(sign[2][i][1]),
                        m), sign[3][i][1]):
                    return 0
                if self.from_poly(self.P(gam1 + gam2), n) != sign[1][i][2] or self.from_poly(self.P(gam2), n) != \
                        sign[1][i][3] or self.H(self.to_int(gam1 + gam2, n, 0)) != sign[1][i][6] or self.H(
                        self.to_int(gam2, n, 0)) != sign[1][i][7]:
                    return 0

        # step 4
        return 1

    def open(self, sign, table):
        # TODO: some membership table
        # TODO: suppouse that verification falls !!!
        # step 1
        # parsing
        # resp = sign[1]
        users = []
        for i in range(rounds):
            # step 2
            del20 = self.P_(self.to_poly(sign[1][i][1]),0)
            del21 = self.P_(self.to_poly(sign[1][i][3]),0)
            if self.H(self.to_int(del20, n, 0)) != sign[1][i][5]:
                del20 = self.P_(self.to_poly(sign[1][i][1]),1)
            if self.H(self.to_int(del21, n, 0)) != sign[1][i][7]:
                del21 = self.P_(self.to_poly(sign[1][i][3]),1)

            del10 = self.P_(self.to_poly(sign[1][i][0]),0)
            if self.H(self.to_int(del10, n, 0)) != sign[1][i][4]:
                del10 = self.P_(self.to_poly(sign[1][i][0]),1)
            del10 -= del20

            del11 = self.P_(self.to_poly(sign[1][i][2]),0)
            if self.H(self.to_int(del11, n, 0)) != sign[1][i][6]:
                del11 = self.P_(self.to_poly(sign[1][i][2]),1)
            del11 -= del21

            # step 3
            nu = del10 + del11

            # step 4
            for user in table:
                is_s = self.to_poly(user[1])
                if is_s == nu:
                    users += user
                    break

        # majority - answer
        return Counter(users).most_common(1)[0][0]

    def join(self, id_):
        # join for one user
        u = GF(q ** m, 'x').random_element()
        k_ = self.k - self.R(u)
        s = self.P_(k_, 0)
        # s_ = from_poly(s, n) + from_poly(u, m) # msk = (u, s_) весь мск есть этот полином
        s_ = self.to_poly(self.from_poly(s, n) + self.from_poly(u, m))  # это в виде полинома
        self.rep.add_user(id_, s_)
        # note that s_ = s || u is solution of P__(z) = P(z) + R(z) = k, P_ - opposite (**-1), P__ - P with _ in up
        # TODO: pk to manager
        return (id_, self.from_poly(s, n), self.from_poly(k_, m))  # mpk = (id, s, k)
