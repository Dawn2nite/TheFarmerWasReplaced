from generatepath import goto_pos


def insertionSortRow(y):
    for x in range(1, get_world_size()):
        goto_pos(x, y)
        currPos = x

        while currPos  > 0:
            currTile = measure()
            move(West)
            prevTile = measure()
            if prevTile > currTile:
                swap(East)
                currPos -= 1
            else:
                move(East)
                break


def insertionSortColumn(x):
    for y in range(1, get_world_size()):
        goto_pos(x, y)
        currPos = y

        while currPos  > 0:
            currTile = measure()
            move(South)
            prevTile = measure()
            if prevTile > currTile:
                swap(North)
                currPos -= 1
            else:
                move(North)
                break

