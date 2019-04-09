"""
Adopted from https://www.tautvidas.com/blog/2018/02/automating-basic-tasks-in-games-with-opencv-and-python/
Date: 04/08/2019
"""

import numpy as np
import time

class Game:

    def __init__(self, controller, observer):
        self.observer = observer
        self.controller = controller

    def refresh(self):
        self.observer.refresh_frame()

    def can_see_object(self, template, threshold=0.9):
        matches = self.observer.find_template(template, threshold=threshold)
        return np.shape(matches)[1] >= 1

    def click_object(self, template, threshold = 0.9, boundingbox = (790, 640, 10, 50), offset=(0, 0)):
        matches = self.observer.find_template(template, threshold)

        if matches[0].size != 0 and matches[1].size != 0:  # if the object is found
            x = (matches[1][0] * self.observer.get_x_ratio()) + offset[0] # (1679 / 800)
            y = (matches[0][0] * self.observer.get_x_ratio()) + offset[1] # * (600 / 1049)
            print("template: " + template + " found at " + str(x) + " " + str(y))

            # TODO define game box
            if x > boundingbox[0] or y > boundingbox[1] or x < boundingbox[2] or y < boundingbox[3]:  # don't click outside out the window
                print("invalid x y, outside clicking box")
            else:
                self.controller.move_mouse(x, y)
                self.controller.left_mouse_click()
        else:
            print("template: " + template + " not found")

    # def click_menu(self):
    #     return self.click_object('menu', offset=(0, 0))

    def click_sun(self):
        # TODO this boundingbox only works when the 800*600 game window is at the top-left coirer of the screen
        return self.click_object('sun_core', threshold = 0.97, boundingbox = (790, 640, 10, 130), offset=(0, 50))


# TODO PROBLEMS