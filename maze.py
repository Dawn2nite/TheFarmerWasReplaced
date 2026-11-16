from generatepath import goto_pos


def opposite(direction):
    if direction == North:
        return South
    elif direction == South:
        return North
    elif direction == East:
        return West
    elif direction == West:
        return East
def neighbor_pos(x, y, direction):
    if direction == North:
        return (x, y + 1)
    if direction == South:
        return (x, y - 1)
    if direction == East:
        return (x + 1, y)
    if direction == West:
        return (x - 1, y)
    
def best_directions(x, y, tx, ty):
    directions = []

    # Toward target
    if tx > x:
        directions.append(East)
    elif tx < x:
        directions.append(West)

    if ty > y:
        directions.append(North)
    elif ty < y:
        directions.append(South)

    # Add ALL remaining directions
    all_directions = [North, East, South, West]

    for direction in all_directions:
        if direction not in directions:
            directions.append(direction)

    return directions
    

def DFS_maze(visited, tx, ty):
    x = get_pos_x()
    y = get_pos_y()
    pos = (x, y)

    visited.add(pos)

    if get_entity_type() == Entities.Treasure:
        return True

    directions = best_directions(x, y, tx, ty)

    for direction in directions:
        next_pos = neighbor_pos(x, y, direction)
        if next_pos in visited:
            continue

        if move(direction):
            if DFS_maze(visited, tx, ty):
                return True

            move(opposite(direction))

    return False
    


def mazeharvest():
    clear()
    goto_pos(0,0)
    while True:
        harvest()    
        plant(Entities.Bush)
        substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
        use_item(Items.Weird_Substance, substance)
        tx ,ty = measure()
        visited = set()
        DFS_maze(visited, tx, ty)
        harvest()

        

def mazesolve():
    directions = [North, East, South, West]
    index = 0
    cont = True
    for i in range(random()*get_world_size()//1):
        move(East)
    for i in range(random()*get_world_size()//1):
        move(North)
    while cont:
        if get_entity_type() == Entities.Treasure:
            harvest()
            plant(Entities.bush)
            use_item(Items.Weird_Substance, get_world_size() * 2**(num_unlocked(Unlocks.Mazes)-1 ))
        else:
            if can_move(directions[(index + 1) % 4]):
                index = (index + 1) % 4
                move(directions[index])
            else:
                if can_move(directions[(index) % 4]):
                    index = (index) % 4
                    move(directions[index])
                else:
                    if can_move(directions[(index - 1) % 4]):
                        index = (index - 1) % 4
                        move(directions[index])
                    else:
                        if can_move(directions[(index + 2) % 4]):
                            index = (index + 2) % 4
                            move(directions[index])

# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    clear()
    for i in range(max_drones()):
        spawn_drone(mazesolve)
    for i in range(5000):
        pass
    while True:
        plant(Entities.bush)
        substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) -1)
        use_item(Items.Weird_Substance, substance)
        mazesolve()
