from snake.model.serpents import Ophion


class Quintus(Ophion):

    def __init__(self, W, H, apples):
        super().__init__(W, H, apples)

    @property
    def name(self):
        return 'Q-Learner (Quintus)'

    def state(self):
        info = self.sensor()
        relative = {
            'behind': [0, 0],
            'ahead': [1, 1],
            'right': [0, 1],
            'left': [1, 0]
        }
        x = relative[info['apple_relative']]
        x.extend([int(d == 0) for d in info['dying_distance']])
        return int(''.join(str(b) for b in x), 2)
