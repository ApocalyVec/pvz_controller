import Solve_and_Update_Gamestate
from Gamestate import Gamestate
import numpy

state = Gamestate()
state.set_field_size(5,7)

plant_mat = numpy.zeros(shape=(3,3), dtype=int)
plant_mat[0] = [1, 50, 0]  # sunflower
plant_mat[1] = [2, 100, 20]  # peashooter
plant_mat[2] = [3, 0, 0]  # empty slot
state.set_plants(plant_mat)

state.add_plant(0, 0, 1)
state.add_plant(0, 1, 1)
state.add_plant(0, 2, 2)
state.add_plant(0, 3, 2)
state.add_plant(0, 4, 2)
# state.add_plant(0, 5, 2)
# state.add_plant(0, 6, 2)

# state.add_plant(1, 2, 2)

state.add_sun(50)

dict = {}
dict[0] = 41
dict[1] = 0
dict[2] = 0
dict[3] = 0
dict[4] = 0
state.set_threats(dict)


sug = Solve_and_Update_Gamestate
sug.solve_and_update_gamestate(state)
