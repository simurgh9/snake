from tkinter import Frame, Canvas, ALL
from pkgutil import get_data
from snake.control import Control
from random import randint
from pprint import pformat


class View(Frame):

    def __init__(self, master):
        byte = get_data(__package__, '../artifacts/title.txt')
        title = byte.decode('utf-8') if byte is not None else 'Snake'

        super().__init__(master)
        self.master = master
        self.master.title(title)
        self.C = Control(self)
        self.master.bind('<Key>', self.C.handle_keyboard)

        w = self.C.M().W * self.C.M().limb_pixel_length
        h = self.C.M().H * self.C.M().limb_pixel_length
        dims = self.pixel_screen_dims()
        # x, y = 0, 0
        x, y = tuple((c2 - c1) // 2 for c1, c2 in zip((w, h), dims))
        self.master.geometry(f'{w}x{h}+{x}+{y}')

        self.pack(fill='both', expand=True)
        self.can = Canvas(self,
                          borderwidth=0,
                          highlightthickness=0,
                          relief='ridge')

        self.snake_colors = [None for _ in self.C.M().snakes]
        for i in range(len(self.snake_colors)):
            r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
            self.snake_colors[i] = f'#{r:02X}{g:02X}{b:02X}'

        self.can.pack()
        self.repaint()

    def repaint(self):
        self.can.delete(ALL)
        self.draw_snakes()
        self.draw_apples()
        # self.draw_debug_info()

        if self.C.advance():
            self.master.after(self.C.M().interval, self.repaint)

    def pixel_screen_dims(self, smaller=False):
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        return width, height

    def draw_lattice(self):
        for i in range(0, self.C.M().W):
            for j in range(0, self.C.M().H):
                x = i * self.C.M().limb_pixel_length
                y = j * self.C.M().limb_pixel_length
                t = self.C.M().limb_pixel_length
                self.can.create_rectangle(x, y, x + t, y + t, outline='white')

    def draw_snakes(self):
        head = 'pink'
        for i, snake in enumerate(self.C.M().snakes):
            limb = self.snake_colors[i]
            for i, j in snake.limbs[1:]:
                fill = limb if not snake.is_dead() else None
                self.draw_point(i, j, limb, fill, self.can.create_rectangle)

            i, j = snake.limbs[0]
            fill = head if not snake.is_dead() else None
            self.draw_point(i, j, head, fill, self.can.create_rectangle)

    def draw_apples(self):
        for i, j in self.C.M().apples:
            self.draw_point(i, j, 'red', 'red', self.can.create_oval)

    def draw_point(self, i, j, color, fill, shape):
        x1 = i * self.C.M().limb_pixel_length
        y1 = j * self.C.M().limb_pixel_length
        x2 = x1 + self.C.M().limb_pixel_length
        y2 = y1 + self.C.M().limb_pixel_length
        shape(x1, y1, x2, y2, outline=color, fill=fill)

    def draw_debug_info(self, lattice=False):
        info = f'{self.C.M().W}x{self.C.M().H}x{self.C.M().limb_pixel_length}'
        snake = self.C.M().snakes[-1]
        info += f'\n{pformat(snake.sensor())}'
        self.can.create_text(0, 0, text=info, anchor='nw')
        if lattice:
            self.draw_lattice()
