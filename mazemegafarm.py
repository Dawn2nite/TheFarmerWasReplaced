# ============================================================
# MULTI-DRONE FRESH-MAZE FARM
#
# Process:
# 1. Clear the field.
# 2. Distribute drones across the field.
# 3. Generate one fresh maze beneath them.
# 4. Every drone runs independent greedy DFS.
# 5. The first drone at the treasure harvests it.
# 6. Other drones detect the gold increase and stop.
# 7. Join all workers and repeat with a new maze.
# ============================================================


# ============================================================
# SETTINGS
#
# 8 columns x 4 rows = 32 distributed starting positions.
# On a 32x32 field:
#
# Horizontal spacing = 4
# Vertical spacing   = 8
# ============================================================

GRID_COLUMNS = 8
GRID_ROWS = 4

DIRECTIONS = [
    North,
    East,
    South,
    West
]


# ============================================================
# DIRECTION HELPERS
# ============================================================

def opposite(direction):
    if direction == North:
        return South

    if direction == South:
        return North

    if direction == East:
        return West

    return East


def neighbor_pos(x, y, direction):
    size = get_world_size()

    if direction == North:
        return (x, (y + 1) % size)

    if direction == South:
        return (x, (y - 1) % size)

    if direction == East:
        return ((x + 1) % size, y)

    return ((x - 1) % size, y)


# ============================================================
# HEURISTIC
#
# Wrapped Manhattan distance is used because the farm's
# coordinates wrap around at the edges.
#
# This only controls which direction DFS tries first.
# All four directions are still eventually considered.
# ============================================================

def axis_distance(a, b):
    size = get_world_size()

    direct_distance = abs(a - b)
    wrapped_distance = size - direct_distance

    if wrapped_distance < direct_distance:
        return wrapped_distance

    return direct_distance


def manhattan_distance(x, y, target_x, target_y):
    return (
        axis_distance(x, target_x)
        +
        axis_distance(y, target_y)
    )


# ============================================================
# DIRECTION ORDERING
#
# Sorts North/East/South/West according to how much closer
# the neighboring tile is to the treasure.
#
# worker_id rotates the original ordering, giving different
# drones different tie-breaking behavior.
# ============================================================

def best_directions(x, y, target_x, target_y, worker_id):
    directions = []

    offset = worker_id % 4

    for i in range(4):
        directions.append(
            DIRECTIONS[(i + offset) % 4]
        )

    # Selection sort the four directions by heuristic distance.
    for i in range(4):
        best_index = i

        for j in range(i + 1, 4):
            best_x, best_y = neighbor_pos(
                x,
                y,
                directions[best_index]
            )

            test_x, test_y = neighbor_pos(
                x,
                y,
                directions[j]
            )

            best_distance = manhattan_distance(
                best_x,
                best_y,
                target_x,
                target_y
            )

            test_distance = manhattan_distance(
                test_x,
                test_y,
                target_x,
                target_y
            )

            if test_distance < best_distance:
                best_index = j

        temporary = directions[i]
        directions[i] = directions[best_index]
        directions[best_index] = temporary

    return directions


# ============================================================
# RECURSIVE GREEDY DFS
#
# Each drone owns a private visited set.
#
# The heuristic only changes exploration order:
# - closest-looking direction first
# - all other directions remain available
#
# starting_gold is used as an environmental completion signal.
# When one drone harvests, the gold total increases, causing
# the other drones to stop.
# ============================================================

def greedy_dfs(
    visited,
    target_x,
    target_y,
    worker_id,
    starting_gold
):
    # Another drone already harvested the treasure.
    if num_items(Items.Gold) > starting_gold:
        return False

    x = get_pos_x()
    y = get_pos_y()

    current = (x, y)

    if current in visited:
        return False

    visited.add(current)

    # This drone found the treasure.
    if get_entity_type() == Entities.Treasure:
        # Protect against two drones arriving almost together.
        if num_items(Items.Gold) == starting_gold:
            harvest()

        return True

    directions = best_directions(
        x,
        y,
        target_x,
        target_y,
        worker_id
    )

    for direction in directions:
        # Stop as soon as another drone wins.
        if num_items(Items.Gold) > starting_gold:
            return False

        next_position = neighbor_pos(
            x,
            y,
            direction
        )

        if next_position in visited:
            continue

        if can_move(direction):
            move(direction)

            found = greedy_dfs(
                visited,
                target_x,
                target_y,
                worker_id,
                starting_gold
            )

            if found:
                return True

            # The maze disappeared after another drone won.
            # Do not try to backtrack through the cleared field.
            if num_items(Items.Gold) > starting_gold:
                return False

            move(
                opposite(direction)
            )

    return False


# ============================================================
# DRONE START POSITIONS
#
# Positions are generated in a snake order so the main drone
# does not need to travel far while deploying workers.
#
# For a 32x32 field:
#
# Row 0: (0,0), (4,0), ... (28,0)
# Row 1: (28,8), (24,8), ... (0,8)
# Row 2: (0,16), ... (28,16)
# Row 3: (28,24), ... (0,24)
# ============================================================

def create_start_positions():
    positions = []

    world_size = get_world_size()

    x_step = world_size // GRID_COLUMNS
    y_step = world_size // GRID_ROWS

    for row in range(GRID_ROWS):
        y = row * y_step

        if row % 2 == 0:
            for column in range(GRID_COLUMNS):
                x = column * x_step
                positions.append((x, y))

        else:
            for column in range(
                GRID_COLUMNS - 1,
                -1,
                -1
            ):
                x = column * x_step
                positions.append((x, y))

    return positions


# ============================================================
# CLEAR-FIELD MOVEMENT
#
# Used only before the maze exists or after it disappears.
# Chooses the shorter wrapped direction on each axis.
# ============================================================

def goto_clear_position(target_x, target_y):
    size = get_world_size()

    while get_pos_x() != target_x:
        current_x = get_pos_x()

        east_distance = (
            target_x - current_x
        ) % size

        west_distance = (
            current_x - target_x
        ) % size

        if east_distance <= west_distance:
            move(East)
        else:
            move(West)

    while get_pos_y() != target_y:
        current_y = get_pos_y()

        north_distance = (
            target_y - current_y
        ) % size

        south_distance = (
            current_y - target_y
        ) % size

        if north_distance <= south_distance:
            move(North)
        else:
            move(South)


# ============================================================
# WORKER
#
# Workers are spawned before the maze exists.
#
# They wait until measure() returns the treasure coordinates.
# do_a_flip() is used instead of "pass" so the worker yields
# execution while waiting.
# ============================================================

def wait_for_maze_and_search(worker_id, starting_gold):
    target = measure()

    while target == None:
        # The maze may have been created and harvested before
        # this worker had a chance to observe it.
        if num_items(Items.Gold) > starting_gold:
            return False

        do_a_flip()

        target = measure()

    target_x, target_y = target

    visited = set()

    return greedy_dfs(
        visited,
        target_x,
        target_y,
        worker_id,
        starting_gold
    )


# ============================================================
# TASK FACTORY
#
# spawn_drone() requires a zero-argument function.
# The factory binds worker_id and starting_gold into that task.
# ============================================================

def make_maze_task(worker_id, starting_gold):
    def task():
        return wait_for_maze_and_search(
            worker_id,
            starting_gold
        )

    return task


# ============================================================
# MAZE CREATION
# ============================================================

def maze_substance_amount():
    maze_level = num_unlocked(
        Unlocks.Mazes
    )

    if maze_level < 1:
        maze_level = 1

    return (
        get_world_size()
        *
        2**(maze_level - 1)
    )


def create_fresh_maze():
    plant(Entities.Bush)

    use_item(
        Items.Weird_Substance,
        maze_substance_amount()
    )


# ============================================================
# JOIN
# ============================================================

def wait_for_all(handles):
    for drone in handles:
        wait_for(drone)


# ============================================================
# ONE COMPLETE FRESH-MAZE CYCLE
# ============================================================

def run_fresh_maze():
    # All workers from the previous round have already been
    # joined before this function is called.
    clear()

    positions = create_start_positions()

    # Main drone starts deployment from position 0.
    start_x, start_y = positions[0]

    goto_clear_position(
        start_x,
        start_y
    )

    starting_gold = num_items(
        Items.Gold
    )

    handles = []

    worker_count = max_drones()

    if worker_count > len(positions):
        worker_count = len(positions)

    # --------------------------------------------------------
    # PRE-POSITION WORKERS
    #
    # Workers 1 through worker_count - 1 are spawned at
    # distributed locations before the maze exists.
    # --------------------------------------------------------

    for worker_id in range(1, worker_count):
        worker_x, worker_y = positions[worker_id]

        goto_clear_position(
            worker_x,
            worker_y
        )

        task = make_maze_task(
            worker_id,
            starting_gold
        )

        drone = spawn_drone(task)

        if drone != None:
            handles.append(drone)

    # --------------------------------------------------------
    # RETURN MAIN DRONE TO ITS ASSIGNED POSITION
    # --------------------------------------------------------

    main_x, main_y = positions[0]

    goto_clear_position(
        main_x,
        main_y
    )

    # --------------------------------------------------------
    # GENERATE THE MAZE BENEATH ALL DISTRIBUTED DRONES
    # --------------------------------------------------------

    create_fresh_maze()

    # Main drone searches too.
    wait_for_maze_and_search(
        0,
        starting_gold
    )

    # --------------------------------------------------------
    # JOIN
    #
    # Other workers stop when they observe the gold increase.
    # Do not create the next maze until all workers exit.
    # --------------------------------------------------------

    wait_for_all(handles)


# ============================================================
# CONTINUOUS FRESH-MAZE FARM
#
# This creates a completely new maze after each harvest.
# It does not reuse the previous maze.
# ============================================================

def maze_megafarm():
    while True:
        run_fresh_maze()


# Direct call is safer than relying on __name__ support in the
# game's restricted Python implementation.
maze_megafarm()