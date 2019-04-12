import pyscreenshot as ImageGrab
import os
import time

from Controller import Controller
from Observer import Observer
from Game import Game

# TODO being able to click on the suns
# TODO being able to plant plants
# TODO know zombies are coming

# TODO define game box: in Game and Observer

# TODO define monitor in observer!!! to fix boundingbox


# API class that does the clicking

# base threat levels of different zombies
zombie_dic = dict()
zombie_dic['normal'] = 200


if __name__ == '__main__':

    boundingBox = (50, 10, 800, 640)
    screenDimension = (1679, 1049)

    controller = Controller()
    observer = Observer(bbox=boundingBox, ssize=screenDimension)
    game = Game(controller, observer)

    # TODO automatically resume game
    time.sleep(2.0)

    start_time = time.time()
    while 1:
        # TODO fix when it can not find the object

        game.refresh()

        game.click_sun()

        normal_z_coords = game.where_are_normal_zombies()
        conehead_z_coords = game.where_are_conehead_zombies()

        if normal_z_coords is not None:
            for nzc in normal_z_coords:
                print("Normal zombie found at: (" + str(nzc[0]) + ", " + str(nzc[1]) + ")")
                # controller.move_mouse(nzc[0], nzc[1])

        if conehead_z_coords is not None:
            for czc in conehead_z_coords:
                print("Conehead zombie found at: (" + str(czc[0]) + ", " + str(czc[1]) + ")")
                # controller.move_mouse(czc[0], czc[1])

        # print("zombie Coord Done")

        current_time = time.time()
        time_since_start = current_time - start_time
        print("one frame done, time since start = " + str(time_since_start))
        time.sleep(0.2)

        print()
        if time_since_start > 50.0:
            break

        # current_time = time.time()
        # time_since_start = current_time - start_time
        #
        # print("time since start is: ", str(time_since_start))
        #
        # if time_since_start < 5.0:
        #     controller.move_mouse(30, 12)
        #     controller.left_mouse_click()

