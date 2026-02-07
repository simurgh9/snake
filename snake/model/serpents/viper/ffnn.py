import numpy as np


class FeedForwardNeuralNetwork:

    def __init__(self, architecture, rng):
        self.rng = rng
        self.architecture = architecture
        self.L = len(architecture) - 1
        self.W, self.b = self.random_weights_biases()

    def __add__(self, mate):
        W = np.empty(self.L, dtype=object)
        b = np.empty(self.L, dtype=object)
        for i in range(self.L):
            c, r = self.architecture[i], self.architecture[i + 1]
            W[i] = np.empty(self.W[i].shape, dtype=self.W[i].dtype)
            mask = self.rng.integers(2, size=(r, c))
            np.putmask(W[i], mask == 0, self.W[i])
            np.putmask(W[i], mask == 1, mate.W[i])
            b[i] = np.empty(self.b[i].shape, dtype=self.b[i].dtype)
            mask = self.rng.integers(2, size=r)
            np.putmask(b[i], mask == 0, self.b[i])
            np.putmask(b[i], mask == 1, mate.b[i])
        child = FeedForwardNeuralNetwork(self.architecture, self.rng)
        child.W, child.b = W, b
        return child

    def __sub__(self, mate):
        W = np.empty(self.L, dtype=object)
        b = np.empty(self.L, dtype=object)
        eta, u, beta = 200, self.rng.uniform(), None
        if u <= 0.5:
            beta = (2 * u)**(1 / (eta + 1))
        else:
            beta = (1 / (2 * (1 - u)))**(1 / (eta + 1))
        for i in range(self.L):
            W[i] = 0.5 * ((1 + beta) * self.W[i] + (1 - beta) * mate.W[i])
            b[i] = 0.5 * ((1 + beta) * self.b[i] + (1 - beta) * mate.b[i])
        child = FeedForwardNeuralNetwork(self.architecture, self.rng)
        child.W, child.b = W, b
        return child

    def __repr__(self):
        ret = ''
        for l, W, b in zip(self.architecture, self.W, self.b):
            ret += '({}: W{} + b{})\n'.format(l, W.shape, b.shape)
        return ret

    def __str__(self):
        return self.__repr__()

    def mutate(self):
        for i in range(self.L):
            c, r = self.architecture[i], self.architecture[i + 1]
            W = self.rng.binomial(1, 0.01, size=(r, c)).astype(np.float64)
            b = self.rng.binomial(1, 0.01, size=r).astype(np.float64)
            self.W[i] = (self.W[i] + W) % 2
            self.b[i] = (self.b[i] + b) % 2

    def random_weights_biases(self, mu=0, sigma=1):
        W = np.empty(self.L, dtype=object)
        b = np.empty(self.L, dtype=object)
        for i in range(self.L):
            c, r = self.architecture[i], self.architecture[i + 1]
            W[i] = self.rng.binomial(1, 0.5, size=(r, c)).astype(np.float64)
            b[i] = self.rng.binomial(1, 0.5, size=r).astype(np.float64)
        return W, b

    def activation(self, x):
        # return 1 / (1 + np.exp(-x))  # sigmoid
        return np.maximum(0, x)  # relu

    def feedforward(self, a, i=0):
        L, W, b = self.L - 1, self.W, self.b
        a = self.activation(W[i] @ a + b[i])
        return a if i == L else self.feedforward(a, i + 1)
