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


def compress_zombie_pos(coords):
    """

    :param coords:
    :return
    """
    if coords is None:
        raise Exception("main.py: compress_zombie_pos: coords given is None")

    xOffset = 50
    yOffset = 50

    actual_coords = []

    x_coords = []
    y_coords = []

    for coord in coords:

        # if len(x_coords) == 0 and len(y_coords) == 0:
        #     isXNew = True
        #     isYNew = True
        # else:
        isXNew = True
        isYNew = True

        for x in x_coords:
            isXNew = isXNew and (not x - xOffset <= coord[0] <= x + xOffset)

        for y in y_coords:
            isYNew = isYNew and (not y - yOffset <= coord[1] <= y + yOffset)

        if isXNew or isYNew:
            x_coords.append(coord[0])
            y_coords.append(coord[1])
            actual_coords.append(coord)

    return actual_coords


def resolve_zom_pos(zom_pos):
    """

    :param zom_pos: the position of the zombies
    :return: (lane, threat_num): int, int
    """
    lane_dic = []

    lane_dic[0] = (0, 60)
    lane_dic[1] = (115, 150)
    lane_dic[2] = ()
    lane_dic[3] = (320, 360)
    lane_dic[4] = ()

    x_pos = zom_pos[0]
    y_pos = zom_pos[1]

    # if <= x_pos


# base threat levels of different zombies
zombie_dic = dict()
zombie_dic['normal'] = 200

if __name__ == '__main__':

    boundingBox = (50, 10, 800, 640)
    screenDimension = (1679, 1049)

    controller = Controller()
    observer = Observer(bbox=boundingBox, ssize=screenDimension)
    game = Game(controller, observer)  # API class that does the clicking

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

            actual_nzc = compress_zombie_pos(normal_z_coords)

            for nzc in actual_nzc:
                print("Normal zombie found at: (" + str(nzc[0]) + ", " + str(nzc[1]) + ")")
                # controller.move_mouse(nzc[0], nzc[1])


        if conehead_z_coords is not None:

            actual_czc = compress_zombie_pos(conehead_z_coords)

            for czc in actual_czc:
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
