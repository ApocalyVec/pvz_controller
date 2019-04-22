import threading

import pyscreenshot as ImageGrab
import os
import time

from Controller import Controller
from Observer import Observer
from Game import Game
import numpy
import Solve_and_Update_Gamestate
from Gamestate import Gamestate

# TODO WE REALLY NEED TO RECOGNIZE SUN COUNT THROUGH CV

lane_dic = dict()

lane_dic[0] = (0, 90)
lane_dic[1] = (115, 170)
lane_dic[2] = (200, 280)
lane_dic[3] = (300, 360)
lane_dic[4] = (380, 500)

normal_z_threat = 100
conehead_z_threat = 200
vaulting_z_threat = 250

is_sunflower_ready = True
is_peashooter_ready = True

sunflower_cd = 5 + 3  # allow 1 sec of wiggle room
peashooter_cd = 5 + 3  # allow 1 sec of wiggle room


def sunflower_cd_ISR():
    global is_sunflower_ready
    is_sunflower_ready = True


def peashooter_cd_ISR():
    global is_peashooter_ready
    is_peashooter_ready = True


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


def resolve_zom_pos(zom_pos, hmax=800):
    """

    :param hmax:
    :param zom_pos: the position of the zombies
    :return: (lane, threat_num): int, float
    """
    global lane_dic

    x_pos = zom_pos[1]
    y_pos = zom_pos[0]

    threat_n = hmax / x_pos

    if lane_dic[0][0] <= y_pos <= lane_dic[0][1]:
        lane_p = 0
    elif lane_dic[1][0] <= y_pos <= lane_dic[1][1]:
        lane_p = 1
    elif lane_dic[2][0] <= y_pos <= lane_dic[2][1]:
        lane_p = 2
    elif lane_dic[3][0] <= y_pos <= lane_dic[3][1]:
        lane_p = 3
    elif lane_dic[4][0] <= y_pos <= lane_dic[4][1]:
        lane_p = 4
    else:
        lane_p = None
        print("main.py: resolve_zom_pos: Failed, check global lane_dic, uncaught y is " + str(y_pos))
        # raise Exception("main.py: resolve_zom_pos: Failed, check global lane_dic, uncaught y is " + str(y_pos))

    return lane_p, threat_n


# base threat levels of different zombies
zombie_dic = dict()
zombie_dic['normal'] = 200

if __name__ == '__main__':

    boundingBox = (50, 10, 800, 640)
    screenDimension = (1679, 1049)

    controller = Controller()
    observer = Observer(bbox=boundingBox, ssize=screenDimension)
    game = Game(controller, observer)  # API class that does the clicking

    ##################
    # Init Game Solver
    state = Gamestate()
    state.set_field_size(5, 7)

    plant_mat = numpy.zeros(shape=(3, 3), dtype=int)
    plant_mat[0] = [1, 50, 0]  # sunflower
    plant_mat[1] = [2, 100, 120]  # peashooter
    plant_mat[2] = [3, 0, 0]  # empty slot
    state.set_plants(plant_mat)
    ##################

    time.sleep(2.0)

    start_time = time.time()
    state.set_sun(50)

    # peashooter_timer = threading.Timer(peashooter_cd, is_peashooter_ready)
    # peashooter_timer.start()

    while 1:

        game.refresh()

        # TODO need to implement digit reg. to get current sun
        if game.click_sun():
            state.add_sun(25)
        print("Current sun is " + str(state.get_sun()))
        time.sleep(0.2)

        """
        Working on zombies
        """
        threat_dic = dict()
        threat_dic[0] = 0
        threat_dic[1] = 0
        threat_dic[2] = 0
        threat_dic[3] = 0
        threat_dic[4] = 0

        normal_z_coords = game.where_are_normal_zombies()
        conehead_z_coords = game.where_are_conehead_zombies()
        vaulting_z_coords = game.where_are_vaulting_zombies()

        if normal_z_coords is not None:

            actual_nzc = compress_zombie_pos(normal_z_coords)

            for nzc in actual_nzc:
                # print("Normal zombie found at: (" + str(nzc[0]) + ", " + str(nzc[1]) + ")")

                lane_present, threat_num = resolve_zom_pos(nzc)
                if lane_present:
                    threat_dic[lane_present] = int(threat_dic[lane_present] + threat_num * normal_z_threat)
                    print("Normal zombie at lane " + str(lane_present) + ", threat num is " + str(threat_num))

        if conehead_z_coords is not None:

            actual_czc = compress_zombie_pos(conehead_z_coords)

            for czc in actual_czc:
                # print("Conehead zombie found at: (" + str(czc[0]) + ", " + str(czc[1]) + ")")
                # controller.move_mouse(czc[0], czc[1])

                lane_present, threat_num = resolve_zom_pos(czc)
                if lane_present:
                    threat_dic[lane_present] = int(threat_dic[lane_present] + threat_num * conehead_z_threat)
                    print("Conehead zombie at lane " + str(lane_present) + ", threat num is " + str(threat_num))

        if vaulting_z_coords is not None:

            actual_vzc = compress_zombie_pos(vaulting_z_coords)

            for vzc in actual_vzc:
                # print("Vaulting zombie found at: (" + str(vzc[0]) + ", " + str(vzc[1]) + ")")

                lane_present, threat_num = resolve_zom_pos(vzc)
                if lane_present:
                    threat_dic[lane_present] = int(threat_dic[lane_present] + threat_num * vaulting_z_threat)
                    print("Vaulting zombie at lane " + str(lane_present) + ", threat num is " + str(threat_num))

        print("Threats:")
        for key, value in threat_dic.items():
            print("lane[" + str(key) + "]: " + str(value))

        # print("zombie Coord Done")
        #
        # sun = game.get_sun() # TODO

        state.set_threats(threat_dic)
        #
        sug = Solve_and_Update_Gamestate
        solution_dict = sug.solve_and_update_gamestate(state)

        # reverse item order in solution dict
        solution_list = []

        for coords, plant_num in solution_dict.items():
            solution_list.append((coords, plant_num))

        solution_list.sort(key=lambda x: x[0][1])  # plant the leftmost plant first
        print(solution_list)

        for coords, plant_num in solution_list:
            if plant_num == 1:
                if is_sunflower_ready:
                    state.remove_sun(game.plant_plant(coords, plant_num))
                    state.add_plant(coords[0], coords[1], plant_num)
                    is_sunflower_ready = False
                    # start timer thread
                    sunflower_timer = threading.Timer(sunflower_cd, sunflower_cd_ISR)
                    sunflower_timer.start()

            if plant_num == 2:
                if is_peashooter_ready:
                    state.remove_sun(game.plant_plant(coords, plant_num))
                    state.add_plant(coords[0], coords[1], plant_num)
                    is_peashooter_ready = False
                    # start timer thread
                    peashooter_timer = threading.Timer(peashooter_cd, peashooter_cd_ISR)
                    peashooter_timer.start()

        current_time = time.time()
        time_since_start = current_time - start_time
        print
        print("one frame done, time since start = " + str(time_since_start))

        print()
        if time_since_start > 180.0:
            break

        # current_time = time.time()
        # time_since_start = current_time - start_time
        #
        # print("time since start is: ", str(time_since_start))
        #
        # if time_since_start < 5.0:
        #     controller.move_mouse(30, 12)
        #     controller.left_mouse_click()
