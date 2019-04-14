from Gamestate import Gamestate
from runtimecsp import RuntimeCsp
from Variable import Variable
from Solver import ac_3
from Solver import backtrack
from Solver import initialize_assignment

import operator

ascii_cap_offset = 65  # offset from 0 based indexes to ascii capital letters
ascii_low_offset = 97  # offset from 0 based indexes to ascii lower case letters


def solve_and_update_gamestate(gamestate):  # take in gamestate
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

    val = update_csp_file(gamestate)
    if val is False:
        return False  # No action necessary
    else:
        field_row = val
        csp = parse_csp("gamestate_csp.txt")
        print("field row: " + str(field_row))
        print("sun budget: " + str(csp.budget))
        print(csp)
        ans = run_csp(csp)
        if ans is False:
            raise Exception("CSP unsolvable, killed")
        else:
            (assignment, csp) = ans
            scrubbed_assignments = remove_redundant_assignments(assignment, gamestate, field_row)
            print(scrubbed_assignments)
            return scrubbed_assignments


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

    for idx in range(len(gamestate.field[highest_threat[0]])):
        file.write(chr(idx + ascii_cap_offset) + "\n")

    file.write("##### - values\n")
    # extract values from plants matrix
    # associate values with sun costs
    for row in gamestate.plants:
        file.write(chr(int(row[0]) + ascii_low_offset) + " " + str(int(row[1])) + "\n")

    file.write("##### - budget constraint\n")
    # sun currently available, plus sun cost of every plant already planted in row
    sun_already_spent = 0
    for idx in range(len(gamestate.field[highest_threat[0]])):
        if gamestate.field[highest_threat[0]][idx] == 0:
            pass
        else:
            sun_already_spent = sun_already_spent + gamestate.plants[gamestate.field[highest_threat[0]][idx] - 1][1]
    file.write(str(gamestate.sun + sun_already_spent) + "\n")

    file.write("##### - threat level\n")
    # current threat level to overcome
    file.write(str(highest_threat[1]) + "\n")

    file.write("##### - attack power\n")
    # available attack power
    file.write((str(gamestate.attack_power(highest_threat[0])) + "\n"))

    file.write("##### - unary inclusive\n")
    # variables that have previously been assigned values have unary inclusive of only their assigned value
    for idx in range(len(gamestate.field[highest_threat[0]])):
        if (idx == 0 or idx == 1) and (gamestate.field[highest_threat[0]][idx] == 0) and (highest_threat[1] > gamestate.attack_power(highest_threat[0])):  # if one of the sunflower tiles is empty but the threat is higher than we can currently handle, don't allow sunflowers to be planted
            file.write((chr(idx + ascii_cap_offset) + " " + chr(3 + ascii_low_offset) + "\n"))
        if (idx > 1) and (gamestate.field[highest_threat[0]][idx] == 0) and (highest_threat[1] <= gamestate.attack_power(highest_threat[0])):  # if one of the peashooter tiles is empty but the threat is lower than we can currently handle, don't allow peashooters to be planted
            file.write((chr(idx + ascii_cap_offset) + " " + chr(3 + ascii_low_offset) + "\n"))
        elif gamestate.field[highest_threat[0]][idx] == 0:
            pass
        else:
            file.write((chr(idx + ascii_cap_offset) + " " + chr(gamestate.field[highest_threat[0]][idx] + ascii_low_offset) + "\n"))


    file.write("##### - unary exclusive\n")
    for idx in range(len(gamestate.field[highest_threat[0]])):
        if idx > 1:  # sunflowers cannot be planted beyond the two leftmost columns
            file.write((chr(idx + ascii_cap_offset) + " " + chr(1 + ascii_low_offset) + "\n"))  # 1 is sunflower
        if idx <= 1:  # peashooters cannot be planted in the two leftmost columns
            file.write((chr(idx + ascii_cap_offset) + " " + chr(2 + ascii_low_offset) + "\n"))  # 2 is peashooter
        # if (highest_threat[1] <= gamestate.attack_power(highest_threat[0])) and (idx > 1):  # if threats are contained, do not plant peashooters # TODO
        #     file.write((chr(idx + ascii_cap_offset) + " " + chr(2 + ascii_low_offset) + "\n"))

    file.write("##### - binary equals\n")
    # NA

    file.write("##### - binary not equals\n")
    # NA

    file.write("##### - binary not simultaneous\n")
    # for columns 3 and greater, if the previous column is empty, a peashooter cannot be planted
    for idx in range(3, len(gamestate.field[highest_threat[0]])):
        file.write((chr(idx + ascii_cap_offset) + " " + chr(idx - 1 + ascii_cap_offset) + " " + chr(2 + ascii_low_offset) + " " + chr(3 + ascii_low_offset) + "\n"))

    file.close()

    return int(highest_threat[0])


def parse_csp(filePath):
    current_section = 0
    p = []
    csp = RuntimeCsp()

    with open(filePath) as input_file:
        for line in input_file:
            if line[0:5] == "#####":  # this line is comment
                current_section += 1
            else:
                arg = line.rstrip().split(" ")
                if current_section == 1:  # reading variables
                    new_tile = Variable(arg[0])
                    csp.add_var_to_graph(new_tile)
                elif current_section == 2:  # reading values
                    p.append(arg[0])
                    csp.add_value(arg[0])
                    csp.add_value_cost(arg[0], arg[1])
                elif current_section == 3:  # deadline
                    csp.make_runtime()
                    budget = int(arg[0])
                    csp.set_budget(budget)
                elif current_section == 4:  # threat level
                    csp.set_threat_level(int(arg[0]))
                elif current_section == 5: # attack power
                    csp.set_attack_power(int(arg[0]))
                elif current_section == 6:  # unary Inclusive
                    const_p = arg[1:len(arg)]
                    csp.add_uin(arg[0], const_p)
                elif current_section == 7:  # unary Exclusive
                    const_p = arg[1:len(arg)]
                    csp.add_uex(arg[0], const_p)
                elif current_section == 8:  # binary equals
                    csp.add_biconst(arg, 1)
                elif current_section == 9:  # binary not equals
                    csp.add_biconst(arg, 0)
                elif current_section == 10:  # binary not simultanious
                    const_var = []
                    const_value = []
                    for i in arg:  # separate the arguments into tasks and processors (values and variables)
                        if i.isupper():  # it is a task if it's an upper case letter
                            const_var.append(i)
                        else:
                            const_value.append(i)

                    csp.add_bins(const_var, const_value)
    return csp


def run_csp(csp):
    if not ac_3(csp):
        print("CSP is AC3 INCONSISTENT, killed")
    print("Variables and their domain after applying Arc Consistency: ")
    csp.print_all_variable()

    assignment = {}  # represent the assignment of variables [Key: Variable, Value: value (str)]

    initialize_assignment(assignment, csp)

    if backtrack(assignment, csp, False) is not None:
        print()
        print("CSP Answer is: ")
        for var, value in assignment.items():
            print(var.name + ": " + value)
        print(str(csp.runtime.get_spending(assignment, csp.value_costs)))
        return (assignment, csp)
    else:
        print("CSP is UNSOLVABLE, killed")
        return False


def remove_redundant_assignments(assignment, gamestate, field_row):
    clean_assignment = {}
    for var, value in assignment.items():
        for col_idx in range(len(gamestate.field[field_row])):
            if (ord(var.name) - ascii_cap_offset == col_idx) and (ord(value) - ascii_low_offset != gamestate.field[field_row][col_idx]):
                if ord(value) - ascii_low_offset != 3:
                    clean_assignment[(field_row, col_idx)] = ord(value) - ascii_low_offset
    return clean_assignment
