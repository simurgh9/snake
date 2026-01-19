from snake.model.serpents import Snake
from math import sqrt, ceil, floor, log2


class Ophion(Snake):

    @property
    def name(self):
        return 'Greedy Player (Ophion)'

    def turn(self):
        info = self.sensor()
        apple_at = info['apple_relative']
        steps_to_collision = info['dying_distance']
        if apple_at == 'left' and steps_to_collision[2] > 0:
            self.turn_left()
        elif apple_at == 'right' and steps_to_collision[1] > 0:
            self.turn_right()
        elif apple_at == 'ahead' and steps_to_collision[0] > 0:
            pass
        else:
            steps = steps_to_collision
            argmax = max(range(len(steps)), key=lambda i: steps[i])
            actions = [lambda: None, self.turn_right, self.turn_left]
            actions[argmax]()

    def sensor(self):
        return {
            'orientation': self.orientation,
            'apple_relative': self.apple_relative(),
            'dying_distance': self.dying_distance()  # ahead, right, left
        }

    def dying_distance(self):
        distances = [0, 0, 0]
        cardinals = [
            self.orientation,
            self.turn_right(True),
            self.turn_left(True)
        ]
        for i, (c1, c2) in enumerate(cardinals):
            x, y = self.limbs[0][0] + c1, self.limbs[0][1] + c2
            while not self.is_dead(x, y, (c1, c2)):
                distances[i] += 1
                x, y = x + c1, y + c2
        return distances

    def apple_relative(self):
        head = self.limbs[0]
        _, apple = self.nearest_apple()
        direction_maps = {
            self.NORTH: {
                'left': lambda h, a: a[0] < h[0],
                'right': lambda h, a: a[0] > h[0],
                'ahead': lambda h, a: a[1] < h[1] or a == h,
                'behind': lambda h, a: a[1] > h[1]
            },
            self.SOUTH: {
                'left': lambda h, a: a[0] > h[0],
                'right': lambda h, a: a[0] < h[0],
                'ahead': lambda h, a: a[1] > h[1] or a == h,
                'behind': lambda h, a: a[1] < h[1]
            },
            self.EAST: {
                'left': lambda h, a: a[1] < h[1],
                'right': lambda h, a: a[1] > h[1],
                'ahead': lambda h, a: a[0] > h[0] or a == h,
                'behind': lambda h, a: a[0] < h[0]
            },
            self.WEST: {
                'left': lambda h, a: a[1] > h[1],
                'right': lambda h, a: a[1] < h[1],
                'ahead': lambda h, a: a[0] < h[0] or a == h,
                'behind': lambda h, a: a[0] > h[0]
            }
        }
        for position, check in direction_maps[self.orientation].items():
            if check(head, apple):
                return position

    def nearest_apple(self):
        distance = float('inf')
        min_idx = -1
        head = self.limbs[0]
        for i, apple in enumerate(self.apples):
            cur_distance = sum([(head[k] - apple[k])**2 for k in [0, 1]])
            if cur_distance < distance:
                distance = cur_distance
                min_idx = i
        return ceil(distance), self.apples[min_idx]
