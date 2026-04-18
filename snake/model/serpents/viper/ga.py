from snake.model import Model
from snake.model.serpents import Viper
from random import choices, random
import numpy as np


class GeneticAlgorithm(Model):

    def __init__(self, width_pixel, height_pixel):
        super().__init__(width_pixel, height_pixel)
        self.interval = 5  # milliseconds
        self.gidx = 0
        rng = np.random.default_rng(0)
        self.snakes = [
            Viper(self.W, self.H, self.apples, rng) for _ in range(1000)
        ]

    def advance(self):
        all_dead = not super().advance()
        if all_dead:
            self.next_generation()
        return True

    def bump_speed(self):
        return

    def next_generation(self):
        self.gidx += 1
        scores = [snake.score() for snake in self.snakes]
        total = sum(scores)
        probs = [score / total for score in scores]
        sorts = sorted(self.snakes, key=lambda x: x.score(), reverse=True)

        mould = '{: 3}. Mean: {: .3f}, Max: {:.3f}'
        print(mould.format(self.gidx, total / len(self.snakes), max(scores)))

        for i in range(len(self.snakes)):
            alice, bob = choices(self.snakes, weights=probs, k=2)
            self.snakes[i] = alice + bob
            if random() < 0.01:
                self.snakes[i].mutate()
            if i < 0.1 * len(self.snakes):
                self.snakes[i].brain = sorts[i].brain
                continue
