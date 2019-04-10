import Solve_and_Update_Gamestate
from Gamestate import Gamestate
import numpy

state = Gamestate()
state.set_field_size(5,7)

plant_mat = numpy.zeros(shape=(2,3), dtype=int)
plant_mat[0] = [1, 50, 0]  # sunflower
plant_mat[1] = [2, 100, 20]  # peashooter
state.set_plants(plant_mat)

state.add_plant(0, 0, 1)
state.add_plant(0, 1, 1)
state.add_plant(0, 2, 2)
state.add_plant(0, 3, 2)
state.add_plant(0, 4, 2)
state.add_plant(0, 5, 2)
state.add_plant(0, 6, 2)

state.add_plant(1, 2, 2)

state.add_sun(200)

dict = {}
dict[0] = 10
dict[1] = 0
dict[2] = 10
dict[3] = 0
dict[4] = 0
state.set_threats(dict)

cont = Solve_and_Update_Gamestate
cont.update_csp_file(state)
