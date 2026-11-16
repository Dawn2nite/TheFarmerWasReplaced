
def goto_pos( x , y ):
    currx = get_pos_x()
    curry = get_pos_y()

    while currx < x:
        if move(East) == False:
            return False
        currx = get_pos_x()
    while curry < y:
        if move(North) == False:
            return False
        curry = get_pos_y()
    while currx > x:
        if move(West) == False:
            return False
        currx = get_pos_x()
    while curry > y:
        if move(South) == False:
            return False
        curry = get_pos_y()


def snake_path():
    path = []
    for y in range(get_world_size()):
        path.append((0, y))
    for y in range(get_world_size() - 1, -1, -1): 
        if y % 2 == 1:
            for x in range(1, get_world_size()):
                path.append((x,y))
        else:
            for x in range(get_world_size() -1, 0, -1):
                path.append((x,y))
    return path

def row_path(origin, width = 0):
    ox, oy = origin
    path = []
    for y in range(oy, oy + width):  
        if y % 2 == 0:
            for x in range(get_world_size()):
                path.append((x,y))
        if y % 2 == 1:
            for x in range(get_world_size() -1 , -1, - 1):
                path.append((x,y))
    return path


def column_path(origin, width = 0):
    ox, oy = origin
    path = []

    for x in range(ox, ox + width):  
        if x % 2 == 0:
            for y in range(get_world_size()):
                path.append((x,y))
        if x % 2 == 1:
            for y in range(get_world_size() -1 , -1, - 1):
                path.append((x,y))
    return path
 
def diagSnakePath(origin=None, square_length=None):
    if origin == None:
        start_x = 0
        start_y = 0
    else:
        start_x, start_y = origin

    if square_length == None:
        square_length = get_world_size()

    path = []

    # A square of length n has 2n - 1 diagonals
    for diagonal in range(2 * square_length - 1):

        diag = []

        for local_x in range(square_length):

            local_y = diagonal - local_x

            if local_y >= 0 and local_y < square_length:
                x = start_x + local_x
                y = start_y + local_y

                diag.append((x, y))

        # Alternate direction
        if diagonal % 2 == 0:
            for i in range(len(diag) - 1, -1, -1):
                path.append(diag[i])
        else:
            for pos in diag:
                path.append(pos)

    return path
    

    
    