"""
Adopted from https://www.tautvidas.com/blog/2018/02/automating-basic-tasks-in-games-with-opencv-and-python/
Date: 04/08/2019
"""

import time
import pyscreenshot as ImageGrab
import os
import time
from pynput.mouse import Button, Controller as MouseController


class Controller:
    def __init__(self):
        self.mouse = MouseController()

    def move_mouse(self, x, y):
        """
        Smoothly move the curvor to (x, y)
        :param x:
        :param y:
        :return: void
        """

        def set_mouse_position(x, y):
            self.mouse.position = (int(x), int(y))

        def smooth_move_mouse(from_x, from_y, to_x, to_y, speed=0.2):
            steps = 40
            sleep_per_step = speed // steps
            x_delta = (to_x - from_x) / steps
            y_delta = (to_y - from_y) / steps
            for step in range(steps):
                new_x = x_delta * (step + 1) + from_x
                new_y = y_delta * (step + 1) + from_y
                set_mouse_position(new_x, new_y)
                time.sleep(sleep_per_step)

        return smooth_move_mouse(
            self.mouse.position[0],
            self.mouse.position[1],
            x,
            y
        )

    def left_mouse_click(self):
        self.mouse.click(Button.left)


    def grab_screen(self, x1, y1, x2, y2):
        """
        This function is disused, we may use MSS to take screenshots
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        """
        # im = ImageGrab.grab(bbox=(0, 50, 800, 640))

        im = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
