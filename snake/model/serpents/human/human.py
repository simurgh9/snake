from snake.model.serpents import Snake


class Human(Snake):

    def __init__(self, W, H, apples):
        super().__init__(W, H, apples)
        self.keys = []

    @property
    def name(self):
        return 'Human Player'

    def turn(self):
        transitions = {
            'up': self.turn_north,
            'right': self.turn_east,
            'down': self.turn_south,
            'left': self.turn_west,
            'l': self.turn_left,  # relative left
            'r': self.turn_right  # relative right
        }
        f = transitions.get(self.dequeue(), lambda: None)
        f()

    def enqueue(self, key):
        self.keys = [key] + self.keys

    def dequeue(self):
        return self.keys.pop() if self.keys else False
