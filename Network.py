import math
import random


class N:
    @staticmethod
    def sig(n):
        return 1 / (1 + math.exp(-n))

    @staticmethod
    def sig_p(n):
        return n * (1 - n)

    @staticmethod
    def mse(y_h, y):
        return (y_h - y) ** 2

    @staticmethod
    def mse_p(y_h, y):
        return y_h - y

    def __init__(self, arch, lr=1):
        self.arch = arch

        self.lr = lr

        self.biases = [[1 for _ in range(arch[la + 1])] for la in range(len(arch) - 1)]
        self.weights = [[[random.random() / math.sqrt(arch[la]) for _ in range(arch[la])] for _ in range(arch[la + 1])] for la in range(len(arch) - 1)]

        print("b", self.biases)
        print("w", self.weights)

        self.bc = [[0 for _ in range(arch[la + 1])] for la in range(len(arch) - 1)]
        self.wc = [[[0 for _ in range(arch[la])] for _ in range(arch[la + 1])] for la in range(len(arch) - 1)]

        self.res = []

    def forward(self, ip):
        self.res = [ip]

        for la in range(len(self.arch) - 1):
            layer_res = []

            for n in range(self.arch[la + 1]):
                neuron_res = self.biases[la][n]

                for c in range(self.arch[la]):
                    neuron_res += ip[c] * self.weights[la][n][c]

                layer_res.append(self.sig(neuron_res))

            self.res.append(layer_res)
            ip = layer_res

        # print(self.res)

        return self.res[-1]

    def backwards(self, y):
        loss = 0

        last_d = []

        for i in range(10):
            loss += self.mse(self.res[-1][i], y[i])

            last_d.append(self.mse_p(self.res[-1][i], y[i]))

        for la in range(len(self.arch) - 1):
            onion = len(self.arch) - 1 - la

            inner_d = []

            for i in range(self.arch[onion]):
                inner_d.append(last_d[i] * self.sig_p(self.res[onion][i]))

            last_d = [0 for _ in range(self.arch[onion - 1])]

            for n in range(self.arch[onion]):
                self.bc[onion - 1][n] += inner_d[n]

                for c in range(self.arch[onion - 1]):
                    self.wc[onion - 1][n][c] += inner_d[n] * self.res[onion - 1][c]
                    last_d[c] += inner_d[n] * self.weights[onion - 1][n][c]

        return loss

    def update(self, its):
        for la in range(len(self.arch) - 1):
            for n in range(self.arch[la + 1]):
                self.biases[la][n] -= self.bc[la][n] * self.lr / its

                self.bc[la][n] = 0

                for c in range(self.arch[la]):
                    self.weights[la][n][c] -= self.wc[la][n][c] * self.lr / its

                    self.wc[la][n][c] = 0
