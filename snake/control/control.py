from snake.model.serpents.viper.ga import GeneticAlgorithm


class Control:

    def __init__(self, view):
        self.allowed_keys = {'up', 'down', 'right', 'left', 'l', 'r', 'space'}
        self.model = GeneticAlgorithm(*view.pixel_screen_dims())

    def M(self):
        return self.model

    def advance(self):
        if self.model.PAUSED:
            return True
        return self.model.advance()

    def handle_keyboard(self, e):
        pressed = e.keysym.lower()
        if pressed in self.allowed_keys:
            if pressed == 'space':
                self.model.toggle_pause()
            else:
                self.model.turn(pressed)
