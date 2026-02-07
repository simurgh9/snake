from snake.model.serpents.ophion import Ophion
from math import sqrt, ceil, floor, log2
from snake.model.serpents.viper.ffnn import FeedForwardNeuralNetwork


class Viper(Ophion):

    def __init__(self, W, H, apples, rng):
        super().__init__(W, H, apples)
        self.age = 0
        self.realestate = set()
        architecture = [len(self.encoded_sensor()), 20, 3]
        self.brain = FeedForwardNeuralNetwork(architecture, rng)

    def turn(self):
        self.age += 1
        tile = self.H * self.limbs[0][1] + self.limbs[0][0]
        if tile not in self.realestate:
            self.realestate.add(tile)
        output = self.brain.feedforward(self.encoded_sensor())
        i, _ = max(enumerate(output), key=lambda x: x[1])
        actions = [lambda: None, self.turn_right, self.turn_left]
        f = actions[i]
        f()

    def score(self):
        a = len(self.limbs) - self.INIT_LEN
        return (1.5**a) + (len(self.realestate) / self.age)

    def is_dead(self, x=None, y=None, orientation=None):
        if (code := super().is_dead(x, y, orientation)):
            return code
        if len(self.realestate) == 0 or self.age == 0:
            return 0
        if (len(self.realestate) / self.age) < 0.6:
            return 3
        return 0

    def encoded_sensor(self):
        info = self.sensor()
        absolute = {
            self.NORTH: [1, 0, 0, 0],
            self.EAST: [0, 1, 0, 0],
            self.SOUTH: [0, 0, 1, 0],
            self.WEST: [0, 0, 0, 1]
        }
        relative = {
            'ahead': [1, 0, 0, 0],
            'right': [0, 1, 0, 0],
            'behind': [0, 0, 1, 0],
            'left': [0, 0, 0, 1]
        }
        x = relative[info['apple_relative']]
        digits = floor(log2(max(self.W, self.H) - 1)) + 1
        for d in info['dying_distance']:
            x.extend([int(b) for b in format(d, f'0{digits}b')])
        return x

    def __add__(self, other):
        ret = Viper(self.W, self.H, self.apples, self.brain.rng)
        ret.brain = ret.brain + other.brain
        return ret

    def mutate(self):
        self.brain.mutate()
