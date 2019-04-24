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

        self.peashooter_card_coords = (122, 92)
        self.sunflower_card_coords = (180, 90)

    def click_target_box(self, x, y):

        x_slope = 80
        y_slope = 100

        x_offset = 35 + x_slope / 2
        y_offset = 180

        x_coord = x_offset + x * x_slope
        y_coord = y_offset + y * y_slope

        self.controller.move_mouse(x_coord, y_coord)
        time.sleep(0.1)
        self.controller.left_mouse_click()
        time.sleep(0.1)
        self.controller.left_mouse_click()
        time.sleep(0.1)
        self.controller.left_mouse_click()


    def refresh(self):
        self.observer.refresh_frame()

    def can_see_object(self, template, threshold=0.9):
        matches = self.observer.find_template(template, threshold=threshold)
        return np.shape(matches)[1] >= 1

    def where_are_objects(self, template, boundingbox=(790, 640, 10, 50), threshold=0.9):
        """

        :param template:
        :param threshold:
        :return a list of xy pairs denoting the positions of the objects within the boundingbox,
                returns None if the object is not found
        """
        matches = self.observer.find_template(template, threshold=threshold)
        x_list = matches[0]
        y_list = matches[1]

        if x_list.size == 0 and y_list.size == 0:
            return None
        else:
            if matches[1].size != matches[0].size:
                raise Exception("x y array size DISMATCH!")

            coord_list = []

            if x_list.size == 1 and y_list.size == 1:
                coord_list.append((x_list[0], y_list[0]))
                return coord_list

            for i in range(int(matches[0].size / 2) - 1):  # iterate through x list and y list
                actual_i = 2 * i
                coord_list.append((x_list[actual_i] / 2, y_list[actual_i] / 2))

            return coord_list

    def where_are_normal_zombies(self):
        return self.where_are_objects('normal_z', threshold=0.8)

    def where_are_conehead_zombies(self):
        return self.where_are_objects('conehead_z', threshold=0.8)

    #
    # def where_are_Flag_zombies(self):
    #
    # TODO vaulting zombie not very recognizable
    def where_are_vaulting_zombies(self):
        return self.where_are_objects('vaulting_z', threshold=0.8)

    def click_object(self, template, threshold=0.9, boundingbox=(790, 640, 10, 50), offset=(0, 0)):
        """

        :param template:
        :param threshold:
        :param boundingbox:
        :param offset:
        :return: True if the object is found and clicked, None otherwise
        """
        matches = self.observer.find_template(template, threshold)

        if matches[0].size != 0 and matches[1].size != 0:  # if the object is found
            x = (matches[1][0] * self.observer.get_x_ratio()) + offset[0]  # (1679 / 800)
            y = (matches[0][0] * self.observer.get_x_ratio()) + offset[1]  # * (600 / 1049)
            print("template: " + template + " found at " + str(x) + " " + str(y))

            # TODO define game box
            if x > boundingbox[0] or y > boundingbox[1] or x < boundingbox[2] or y < boundingbox[
                3]:  # don't click outside out the window
                print("invalid x y, outside clicking box")
            else:
                time.sleep(0.1)
                self.controller.move_mouse(x, y)
                self.controller.left_mouse_click()
                time.sleep(0.1)
                self.controller.move_mouse(x + 10, y + 10)
                self.controller.left_mouse_click()
                time.sleep(0.1)
                self.controller.move_mouse(x + 30, y + 30)
                self.controller.left_mouse_click()

                # something has been clicked
                return True
            # else:
            print("template: " + template + " not found")

    # def click_menu(self):
    #     return self.click_object('menu', offset=(0, 0))

    def plant_plant(self, coords, plant_num):
        """
\
        :param plant_num: 0 = sunflower, 1 = peashooter
        :param coords:
        """

        if plant_num == 1:
            card_coords = self.sunflower_card_coords
            cost = 50
        elif plant_num == 2:
            card_coords = self.peashooter_card_coords
            cost = 100
        else:
            raise Exception("Game.py: plant_plant: unrecognized plant num")

        self.controller.move_mouse(card_coords[0], card_coords[1])
        time.sleep(0.2)
        self.controller.left_mouse_click()
        time.sleep(0.2)

        self.click_target_box(coords[1], coords[0])  # y comes first in the tuple

        return cost

    def click_sun(self):
        # TODO this boundingbox only works when the 800*600 game window is at the top-left coirer of the screen
        if self.click_object('sun_core', threshold=0.98, boundingbox=(790, 640, 10, 130), offset=(10, 60)):
            # self.click_object('sun_core', threshold=0.98, boundingbox=(790, 640, 10, 130), offset=(15, 70))
            # self.click_object('sun_core', threshold=0.98, boundingbox=(790, 640, 10, 130), offset=(20, 80))
            return True

    def floor_1(self, num):
        if num <= 0:
            return 0;
        else:
            return num

    # def get_sun(self):
    # self.observer

# TODO PROBLEMS
