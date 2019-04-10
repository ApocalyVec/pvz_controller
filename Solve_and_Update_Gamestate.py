import numpy
from Gamestate import Gamestate
import operator

def solve_and_update_gamestate(gamestate): # take in gamestate
    """
    takes in parameters representing the current gamestate and returns which plants to buy and where to plant them
    :param Gamestate gamestate: the current game state
    :return: dictionary, keys are tiles, values are plants
    """

    # goal: on most threatened row, raise atk power until >= threat level.
    #   If sun or space runs out, raise atk power as much as possible with available resources.
    #   If excess sun after raising atk power, raise atk power on next most threatened row.
    #   If atk power in all rows is greater than threat level, purchase sunflowers
    #   If no remaining space for sunflowers, do nothing

    if update_csp_file(gamestate) is False:
        return False  # No action necessary
    # else:
    #     purchase_dict = solve_csp("gamestate_csp.txt")
    #     return purchase_dict


def update_csp_file(gamestate):
    # Call this function to update gamestate_csp.text

    # sort field rows by threat level, store sorted rows in queue
    sorted_threats_queue = sorted(gamestate.threats.items(), key=operator.itemgetter(1), reverse=True)

    highest_threat = []

    while len(sorted_threats_queue) != 0:
        highest_threat = sorted_threats_queue.pop(0)  # select the most threatened row with deficient attack power and available tiles
        if (highest_threat[1] > gamestate.attack_power(highest_threat[0])) and (gamestate.room_for_attack(highest_threat[0])):
            break
        else:
            highest_threat = []

    if highest_threat == []:  # if all attack powers are greater than or equal to threat levels
        if gamestate.room_for_sunflowers():
            highest_threat = [gamestate.sunflower_row(), 0]  # plant sunflowers if there is room
        else:
            return False  # do nothing if there is no room

    with open("gamestate_csp.txt", "w"):  # Create a txt file representing the csp for the popped row
        pass

    file = open("gamestate_csp.txt", "w")

    file.write("##### - variables\n")
    # each tile in the field row is one variable
    # variables are not associated with a cost
    ascii_cap_offset = 65  # offset from 0 based indexes to ascii capital letters
    ascii_low_offset = 97  # offset from 0 based indexes to ascii lower case letters
    for idx in range(len(gamestate.field[highest_threat[0]])):
        file.write(chr(idx + ascii_cap_offset) + "\n")

    file.write("##### - values\n")
    # extract values from plants matrix
    # associate values with sun costs
    for row in gamestate.plants:
        file.write(chr(int(row[0]) + ascii_low_offset) + " " + str(int(row[1])) + "\n")

    file.write("##### - budget constraint\n")
    # sun currently available
    file.write(str(gamestate.sun) + "\n")

    file.write("##### - unary inclusive\n")
    # variables that have previously been assigned values have unary inclusive of only their assigned value
    for idx in range(len(gamestate.field[highest_threat[0]])):
        if gamestate.field[highest_threat[0]][idx] == 0:
            pass
        else:
            file.write((chr(idx + ascii_cap_offset) + " " + chr(gamestate.field[highest_threat[0]][idx] + ascii_low_offset) + "\n"))

    file.write("##### - unary exclusive\n")
    for idx in range(len(gamestate.field[highest_threat[0]])):
        if idx > 1:  # sunflowers cannot be planted beyond the two leftmost columns
            file.write((chr(idx + ascii_cap_offset) + " " + chr(1 + ascii_low_offset) + "\n"))  # 1 is sunflower
        if idx <= 1:  # peashooters cannot be planted in the two leftmost columns
            file.write((chr(idx + ascii_cap_offset) + " " + chr(2 + ascii_low_offset) + "\n"))  # 2 is peashooter

    file.write("##### - binary equals\n")
    # NA

    file.write("##### - binary not equals\n")
    # NA

    file.write("##### - binary not simultaneous\n")
    # NA

    file.close()

    return int(highest_threat[0])
