def till_if_needed(plant_type):
    tilledPlants = [Entities.Carrot, Entities.Pumpkin, Entities.Cactus, Entities.Sunflower]
    if plant_type in tilledPlants and get_ground_type() == Grounds.Grassland:
        till()

def water_if_needed():
    if get_water() < 0.75:
        use_item(Items.Water)

def harvest_and_plant(plant_type):
    if can_harvest():
        harvest()
    till_if_needed(plant_type)
    plant(plant_type)
    if get_entity_type() == None:
        till_if_needed(plant_type)
        plant(plant_type)
        

def general_harvest():
    halfworld = get_world_size() // 2

    x = get_pos_x()
    y = get_pos_y()
    
    if x  < halfworld and y < halfworld:
        harvest_and_plant(Entities.Grass)
    if y >= halfworld:
        if y % 2 == 0:
            if x % 2 == 0:
                harvest_and_plant(Entities.Tree)
            else:
                harvest_and_plant(Entities.Bush)
        else:
            if x % 2 == 1:
                harvest_and_plant(Entities.Tree)
            else:
                harvest_and_plant(Entities.Bush)
    if x >= halfworld and y < halfworld:
        harvest_and_plant(Entities.Carrot)

def polyCulture(requests):
    curr = (get_pos_x(), get_pos_y())

    water_if_needed()

    # Harvest mature current plant
    if can_harvest():
        harvest()

    # ---------------------------------
    # Priority 1: fulfill a request here
    # ---------------------------------

    if curr in requests:
        crop = requests.pop(curr)

        till_if_needed(crop)
        plant(crop)

    # ---------------------------------
    # Priority 2: plant default crop
    # ---------------------------------

    else:
        till_if_needed(Entities.Carrot)
        plant(Entities.Carrot)

    # ---------------------------------
    # Record this new plant's request
    # ---------------------------------

    companion = get_companion()

    if companion != None:
        crop, target = companion

        # Avoid replacing an existing request
        if target not in requests:
            requests[target] = crop