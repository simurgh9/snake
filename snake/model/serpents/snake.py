from abc import ABC, abstractmethod


class Snake(ABC):

    EAST = (1, 0)
    WEST = (-1, 0)
    SOUTH = (0, 1)
    NORTH = (0, -1)
    INIT_LEN = 5
    RIGHTS = {  # if you face k, v is to your right
        NORTH: EAST,
        EAST: SOUTH,
        SOUTH: WEST,
        WEST: NORTH
    }

    def __init__(self, W, H, apples):
        self.keys = []
        self.apples = apples
        self.W, self.H = W, H
        self.orientation = self.EAST
        self.limbs = [(self.W // 2, self.H // 2)]
        for _ in range(self.INIT_LEN - 1):
            self.limbs.append((self.limbs[-1][0] - 1, self.limbs[-1][1]))

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def turn(self):
        pass

    def advance(self):
        self.turn()
        replaced_limb_x = self.limbs[0][0] + self.orientation[0]
        replaced_limb_y = self.limbs[0][1] + self.orientation[1]
        self.limbs.insert(0, (replaced_limb_x, replaced_limb_y))
        if self.limbs[0] in self.apples:
            return self.apples.index(self.limbs[0])
        self.limbs.pop()
        return None

    def respawn(self):
        self.orientation = self.EAST
        self.limbs = [(self.W // 2, self.H // 2)]
        for _ in range(self.INIT_LEN - 1):
            self.limbs.append((self.limbs[-1][0] - 1, self.limbs[-1][1]))

    def score(self):
        return len(self.limbs) - self.INIT_LEN

    def is_dead(self, x=None, y=None, orientation=None):
        if x is None and y is None:
            x, y = self.limbs[0]
        if orientation is None:
            orientation = self.orientation
        if x < 0 or x >= self.W or y < 0 or y >= self.W:
            return 1  # died by wall collision
        if (x, y) in self.limbs[1:]:
            return 2  # died by limb collision
        return 0  # is alive

    def turn_north(self):
        self.orientation = self.NORTH

    def turn_south(self):
        self.orientation = self.SOUTH

    def turn_west(self):
        self.orientation = self.WEST

    def turn_east(self):
        self.orientation = self.EAST

    def turn_left(self, eval_only=False):
        lefts = {v: k for k, v in self.RIGHTS.items()}
        if not eval_only:
            self.orientation = lefts[self.orientation]
        return lefts[self.orientation]

    def turn_right(self, eval_only=False):
        if not eval_only:
            self.orientation = self.RIGHTS[self.orientation]
        return self.RIGHTS[self.orientation]
