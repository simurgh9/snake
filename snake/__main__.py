from tkinter import Tk
from snake.view import View


def main():
    root = Tk()
    root.tk.call('tk', 'scaling', 6.0)
    view = View(root)
    view.mainloop()


if __name__ == '__main__':
    main()
