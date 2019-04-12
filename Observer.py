"""
Adopted from https://www.tautvidas.com/blog/2018/02/automating-basic-tasks-in-games-with-opencv-and-python/
Date: 04/08/2019
"""

import cv2
import os
from mss import mss
from PIL import Image
import numpy as np
import time


class Observer:
    def __init__(self, bbox=(50, 10, 800, 640), ssize=(1679, 1049)):
        # all the in game assets
        self.image_assets = {
            'sun': 'assets/sun.png',
            'sun_core': 'assets/sun_core.png',
            'menu': 'assets/menu.png',

            # zombies
            'normal_z': 'assets/zombies/normal_z.png',
            'conehead_z': 'assets/zombies/conehead_z.png'
        }

        # TODO
        # self.xRatio, self.yRatio = (bbox[2] - bbox[1]) / ssize[0], (bbox[3] - bbox[0]) / ssize[1]
        self.xRatio, self.yRatio = 1/2, 1/2

        self.image_template = {k: cv2.imread(v, 0) for (k, v) in self.image_assets.items()}
        self.monitor = {'top': bbox[0], 'left': bbox[1], 'width': bbox[2], 'height': bbox[3]}  # grab the entire screen
        self.screen = mss()

        #  volatile object that contains the latest screenshot
        self.frame = None

    @staticmethod
    def convert_rgb_to_bgr(img):
        return img[:, :, ::-1]

    def get_x_ratio(self):
        """

        :return: float: x ratio
        """
        return self.xRatio

    def get_x_ratio(self):
        """

        :return: float: y ratio
        """
        return self.yRatio

    def grab_screen(self):
        """
        grab a screenshot, convert it to grayscale
        :return: the array representation of the screenshot in grayscale
        """
        sct_img = self.screen.grab(self.monitor)
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img = np.array(img)
        img = self.convert_rgb_to_bgr(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # img_gray_png = Image.fromarray(img_gray)
        # img_gray_png.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')

        return img_gray

    def refresh_frame(self):
        """
        update the frame attribute to the latest screenshot
        """
        self.frame = self.grab_screen()

    def match_template(self, template, threshold):
        # self.convert_rgb_to_bgr(template)
        res = cv2.matchTemplate(self.frame, template, cv2.TM_CCOEFF_NORMED)
        matches = np.where(res >= threshold)
        return matches

    def find_template(self, name, threshold):
        """
        find the matching point from our defined template domain
        :param name:
        :param image:
        :param threshold:
        """
        # if image is None:
        #     if self.frame is None:
        #         self.refresh_frame()
        #     image = self.frame

        return self.match_template(self.image_template[name], threshold)
