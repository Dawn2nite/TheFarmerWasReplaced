from generatepath import goto_pos
import harvestlib
import sort
import generatepath
import maze

halfworld = get_world_size()//2



def polyHarvest(path):
    polyDict = {}
    while True:
        for x, y in path:
            goto_pos(x,y)
            harvestlib.polyCulture(polyDict)

def pumpkin_plant(path):
    for x, y in path:
        goto_pos(x,y)
        harvestlib.harvest_and_plant(Entities.Pumpkin)
    return path

def replant_pumpkin(path):
    while len(path) != 0:
        
        revist = []       
        for x, y in path:
            goto_pos(x,y)
            harvestlib.water_if_needed()
            while not can_harvest() and get_entity_type() == Entities.Pumpkin:
                if get_entity_type() == Entities.Dead_Pumpkin:
                    plant(Entities.Pumpkin)
                    revist.append((get_pos_x(), get_pos_y()))
                    break
                do_a_flip()    
            if get_entity_type() != Entities.Pumpkin:
                plant(Entities.Pumpkin)
                revist.append((get_pos_x(), get_pos_y()))

        path = revist   

def plantCactus(path):
    for x, y in path:
        goto_pos(x, y)
        harvestlib.harvest_and_plant(Entities.Cactus)

    # Bigharvest(path, harvestlib.general_harvest)
    # pumpkin_harvest(path)

def cactusharvest(path):
    plantCactus(path)
    for y in range(get_world_size()):
        sort.insertionSortRow(y)
    for x in range(get_world_size()):
        sort.insertionSortColumn(x)

def dinosaurharvest(path = None):
    clear()
    set_world_size(10)
    if path == None:
        path = generatepath.snake_path()

    change_hat(Hats.Straw_Hat)
    path = generatepath.snake_path()
    goto_pos(0,0)
    change_hat(Hats.Dinosaur_Hat)
    while True:
        for x, y in path:
            if goto_pos(x,y) == False:
                break
        if goto_pos(0, 0) == False:
            break



if __name__ == "__main__":
    path = generatepath.snake_path()
        # polyHarvest(path)
        # pumpkin_plant(path)
        # cactusharvest(path)
        # dinosaurharvest(path)
        # sunflower.sunflowerHarvset(path)
        # maze.mazeharvest()
