import generatepath
import harvestlib


# ============================================================
# SETTINGS
# ============================================================

BLOCK_SIZE = 5
GAP_SIZE = 1

# Distance from the start of one block to the next
STRIDE = BLOCK_SIZE + GAP_SIZE


# ============================================================
# GENERATE 5x5 BLOCK ORIGINS
#
# 32x32 world:
#
# (0,0)   (6,0)   (12,0)   (18,0)   (24,0)
# (0,6)   (6,6)   ...
# ...
#
# Creates 25 independent 5x5 pumpkin farms.
# ============================================================

def create_pumpkin_origins():
    origins = []
    n = get_world_size()

    for y in range(
        0,
        n - BLOCK_SIZE + 1,
        STRIDE
    ):
        for x in range(
            0,
            n - BLOCK_SIZE + 1,
            STRIDE
        ):
            origins.append((x, y))

    return origins


# ============================================================
# GENERATE SNAKE PATH THROUGH ONE 5x5 BLOCK
#
# Example:
#
# → → → → →
#         ↓
# ← ← ← ← ←
# ↓
# → → → → →
#
# ============================================================

def create_block_path(origin):
    start_x, start_y = origin

    path = []

    for row in range(BLOCK_SIZE):
        y = start_y + row

        # Left -> Right
        if row % 2 == 0:

            for x in range(
                start_x,
                start_x + BLOCK_SIZE
            ):
                path.append((x, y))

        # Right -> Left
        else:

            for x in range(
                start_x + BLOCK_SIZE - 1,
                start_x - 1,
                -1
            ):
                path.append((x, y))

    return path


# ============================================================
# PLANT INITIAL PUMPKINS
# ============================================================

def plant_pumpkin_block(path):

    for x, y in path:

        generatepath.goto_pos(x, y)

        harvestlib.till_if_needed(
            Entities.Pumpkin
        )

        if get_entity_type() != Entities.Pumpkin:

            plant(
                Entities.Pumpkin
            )


# ============================================================
# REPAIR / WAIT
#
# Only failed or immature pumpkins are revisited.
#
# Example:
#
# 25
# ↓
# 6 remaining
# ↓
# 2 remaining
# ↓
# 0
#
# ============================================================

def repair_pumpkin_block(path):

    remaining = path

    while len(remaining) != 0:

        revisit = []

        for x, y in remaining:

            generatepath.goto_pos(x, y)
            harvestlib.water_if_needed()

            entity = get_entity_type()


            # ------------------------------------
            # Dead pumpkin
            # ------------------------------------

            if entity == Entities.Dead_Pumpkin:

                plant(
                    Entities.Pumpkin
                )

                revisit.append(
                    (x, y)
                )


            # ------------------------------------
            # Pumpkin missing entirely
            # ------------------------------------

            elif entity != Entities.Pumpkin:

                harvestlib.till_if_needed(
                    Entities.Pumpkin
                )

                plant(
                    Entities.Pumpkin
                )

                revisit.append(
                    (x, y)
                )


            # ------------------------------------
            # Pumpkin exists but isn't mature
            # ------------------------------------

            elif not can_harvest():

                revisit.append(
                    (x, y)
                )


            # ------------------------------------
            # Otherwise:
            #
            # Pumpkin exists AND is mature.
            # Don't revisit it.
            # ------------------------------------


        remaining = revisit


# ============================================================
# ONE COMPLETE 5x5 PUMPKIN CYCLE
# ============================================================

def pumpkin_cycle(path):

    # -------------------------
    # Phase 1
    # Plant 25 pumpkins
    # -------------------------

    plant_pumpkin_block(path)


    # -------------------------
    # Phase 2
    # Repair failures until
    # everything is ready
    # -------------------------

    repair_pumpkin_block(path)


    # -------------------------
    # Phase 3
    # Harvest merged pumpkin
    # -------------------------

    x, y = path[0]

    generatepath.goto_pos(
        x,
        y
    )

    harvest()


# ============================================================
# PERMANENT WORKER
#
# Each drone owns exactly one block.
# ============================================================

def pumpkin_worker(path):

    while True:

        pumpkin_cycle(path)


# ============================================================
# TASK FACTORY
#
# spawn_drone() needs a zero-argument function.
# ============================================================

def make_pumpkin_task(path):

    def task():

        pumpkin_worker(path)

    return task


# ============================================================
# MEGAFARM
# ============================================================

def pumpkinMegaFarm():

    clear()

    origins = create_pumpkin_origins()

    paths = []

    # ----------------------------------------
    # Generate all 25 worker paths
    # ----------------------------------------

    for origin in origins:

        path = create_block_path(
            origin
        )

        paths.append(path)


    # ----------------------------------------
    # Spawn workers for blocks 1-24
    #
    # 24 spawned drones
    # +
    # 1 main drone
    # =
    # 25 workers
    # ----------------------------------------

    for i in range(1, len(paths)):

        task = make_pumpkin_task(
            paths[i]
        )

        spawn_drone(task)


    # ----------------------------------------
    # Main drone owns block 0
    # ----------------------------------------

    main_task = make_pumpkin_task(
        paths[0]
    )

    main_task()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    pumpkinMegaFarm()