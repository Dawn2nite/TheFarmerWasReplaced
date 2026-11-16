from generatepath import goto_pos
from harvestlib import harvest_and_plant
import harvestlib
def sunflower_plantMeasure(path):
    sunflowerList = []
    for i in range(16):
        sunflowerList.append([])

    for x, y in path:
        goto_pos(x,y)
        harvest_and_plant(Entities.Sunflower)
        harvestlib.water_if_needed()
        petals = measure()
        sunflowerList[petals].append((x,y))
    return sunflowerList

def sunflower_harvest(sunflowerList, petals):
    for j in range(len(sunflowerList[petals])):
        x, y  = sunflowerList[petals][j]
        goto_pos(x, y)     
        harvestlib.water_if_needed()
        while not can_harvest():
            do_a_flip()
        harvest()

