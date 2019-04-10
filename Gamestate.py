import numpy


class Gamestate:
    def __init__(self):
        self.field = None  # n by m matrix representing the tiles of the field and any plants on the tiles.
        self.plants = None  # n by 3 matrix representing purchasable plants. Col 0 is plant number (one indexed, 1 = sunflower, 2 = peashooter). Col 1 is plant cost. Col 2 is plant attack power
        self.sun = 0  # current sun resources
        self.threats = {}  # dictionary with field row numbers as keys and threat levels as values

    # returns true if there is room for more sunflowers on the field
    def room_for_sunflowers(self):
        for row in self.field:
            if row[0] == 0 or row[1] == 0:
                return True
        return False

    # returns a row that can hold more sunflowers. ONLY CALL THIS AFTER CONFIRMING A ROW WITH ROOM EXISTS
    def sunflower_row(self):
        for idx in range(len(self.field)):
            if self.field[idx][0] == 0 or self.field[idx][1] == 0:
                return idx
        return False

    # returns true if a given field row has more room for attacking plants
    def room_for_attack(self, row):
        for col in range(2, len(self.field[0])):
            if self.field[row][col] == 0:
                return True
        return False

    def set_field_size(self, rows, columns):
        self.field = numpy.zeros(shape=(rows, columns), dtype=int)

    def add_plant(self, row, col, plant_num):
        self.field[row, col] = plant_num

    def set_plants(self, plant_mat):
        self.plants = plant_mat

    def set_threats(self, threat_dict):
        self.threats.clear()
        self.threats = threat_dict

    def add_sun(self, new_sun):
        self.sun = self.sun + new_sun

    def attack_power(self, row):
        atk = 0
        for col in range(len(self.field[0])):
            if self.field[row][col] != 0:
                atk = atk + self.plants[self.field[row][col] - 1][2]
        return atk

