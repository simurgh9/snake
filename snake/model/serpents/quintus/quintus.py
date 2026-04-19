import numpy as np
from snake.model.serpents import Ophion

# 5 bit state:
#    apple_bit, apple_bit, danger_ahead, danger_right, danger_left
# 3 actions: ahead, right, left
# Reference: Tom Mitchell, Machine Learning, section 13.3.2 (pg. 374)

class Quintus(Ophion):

    STANDARD_REWARD = 1

    def __init__(self, W, H, apples):
        super().__init__(W, H, apples)
        self.gamma = 0.8
        self.Q = np.zeros((32, 3))
        self.actions = [lambda: None, self.turn_right, self.turn_left]

    @property
    def name(self):
        return 'Q-Learner (Quintus)'

    def turn(self):
        state = self.state()
        action_index = np.argmax(self.Q[state])
        self.actions[action_index]()
        return state, action_index

    def advance(self):
        ret = None
        distance_before, _ = self.nearest_apple()
        state, action = self.turn()
        replaced_limb_x = self.limbs[0][0] + self.orientation[0]
        replaced_limb_y = self.limbs[0][1] + self.orientation[1]
        self.limbs.insert(0, (replaced_limb_x, replaced_limb_y))
        distance_after, _ = self.nearest_apple()

        if self.limbs[0] in self.apples:
            ret = self.apples.index(self.limbs[0])
        else:
            self.limbs.pop()

        reward = self.reward(distance_before, distance_after)
        new_state = self.Q[self.state()]
        self.Q[state][action] = reward + (self.gamma * np.argmax(new_state))

        if self.is_dead() > 0:
            self.reset()  # we never die, we respawn with the same self.Q

        return ret

    def state(self):
        info = self.sensor()
        apple = {'behind': '00', 'ahead': '11', 'right': '01', 'left': '10'}
        x = apple[info['apple_relative']]
        x += ''.join(str(int(d <= 0)) for d in info['dying_distance'])
        return int(x, 2)

    def reward(self, before, after):
        if self.limbs[0] in self.apples:
            return self.STANDARD_REWARD
        if self.is_dead() > 0:
            return -100*self.STANDARD_REWARD
        if after < before:
            return 0.1*self.STANDARD_REWARD
        if after >= before:
            return -0.1*self.STANDARD_REWARD

    def reset(self):
        self.orientation = self.EAST
        self.limbs = [(self.W // 2, self.H // 2)]
        for _ in range(self.INIT_LEN - 1):
            self.limbs.append((self.limbs[-1][0] - 1, self.limbs[-1][1]))
