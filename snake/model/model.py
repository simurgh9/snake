import snake.model.serpents as serpents
from inspect import getmembers, isclass
from math import log, floor
from random import seed, randint


class Model:

    EXPONENT = 7

    def __init__(self, width_pixel, height_pixel):
        seed(42)
        self.PAUSED = False
        self.interval = 250  # milliseconds
        w, h, limb = self.pixel_to_blocks(width_pixel, height_pixel)
        self.W, self.H, self.limb_pixel_length = w, h, limb

        # initialise apples
        self.apples = [None for i in range(100)]
        for i in range(len(self.apples)):
            self.replenish_apple(i, speedup=False)

        # initialise snakes
        self.snakes = []
        agents = {c.__name__: c for _, c in getmembers(serpents, isclass)}
        for i, name in enumerate(agents):
            if name not in ['Snake', 'Viper']:
                Agent = agents[name]
                self.snakes.append(Agent(self.W, self.H, self.apples))
                print(f'[x] {self.snakes[-1].name:10s} initialised.')

    def advance(self):
        living = []
        for snake in self.snakes:
            living.append(snake.is_dead() == 0)
            if living[-1]:
                eaten_apple_index = snake.advance()
                self.replenish_apple(eaten_apple_index)
        return any(living)

    def turn(self, pressed):
        for snake in self.snakes:
            if isinstance(snake, serpents.Human):
                snake.enqueue(pressed)
                break

    def toggle_pause(self):
        self.PAUSED = not self.PAUSED
        return self.PAUSED

    def replenish_apple(self, i, speedup=True):
        if i is not None:
            self.apples[i] = self.random_apple()
            if speedup:
                self.bump_speed()

    def bump_speed(self):
        self.interval = int(max(0.9 * self.interval, 1))

    def random_apple(self):
        i, j = randint(0, self.W - 1), randint(0, self.H - 1)
        if not hasattr(self, 'snakes'):
            return (i, j)
        if not (self.is_limb(i, j) or (i, j) in self.apples):
            return (i, j)
        return self.random_apple()

    def is_limb(self, i, j):
        for snake in self.snakes:
            if not snake.is_dead() and (i, j) in snake.limbs:
                return True
        return False

    def pixel_to_blocks(self, width, height):
        width, height = width // 2, height // 2
        # comment the line bellow if you don't want a square window
        height = width if height < width else height
        # we make length a power of two so we can divide it by a power
        # of two and break the screen up in equilength blocks.
        w, h = (2**floor(log(length, 2)) for length in (width, height))
        limb = int(2**(log(min(w, h), 2) - self.EXPONENT))
        return w // limb, h // limb, limb
