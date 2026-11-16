import main
import sort
import generatepath
import harvestlib
import generatepath
import sunflower

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def create_column_path():
    paths = []
    drone_count = max_drones()
    
    width = get_world_size() // drone_count   # 4

    for i in range(drone_count):
        origin = (i * width, 0)
        path = generatepath.column_path(origin, width)
        paths.append(path)
    return paths

def create_row_path():
    paths = []

    drone_count = max_drones()
    width = get_world_size() // drone_count   # 4

    for i in range(drone_count):
        origin = (0, i * width )
        path = generatepath.row_path(origin, width)
        paths.append(path)
    return paths

def fork_join(tasks):
    handles = []
        
    for i  in range(1, len(tasks)): 
        drone = spawn_drone(tasks[i])

        if drone != None:
            handles.append(drone)
    main_result = tasks[0]()
    results = [main_result]
    for drone in handles:
        result = wait_for(drone)
        results.append(result)

    return results
# ============================================================
# SYNCHRONIZATION
# ============================================================

def wait_all(handles):
    for drone in handles:
        if drone != None:
            wait_for(drone)


# ============================================================
# CACTUS FARM
# ============================================================

def make_row_task(path):
    def task():
        for x, y in path:
            generatepath.goto_pos(x, y)
            harvestlib.harvest_and_plant(Entities.Cactus)
        x, y = path[0]
        sort.insertionSortRow(y)
    return task

def make_column_task(path):
    def task():
        x, y = path[0]  
        sort.insertionSortColumn(x)
    return task


def cactus_farm():
    while True:
        paths = create_row_path()

        task = []
        for path in paths:
            task.append(make_row_task(path))
        fork_join(task)

        paths = create_column_path()
        task = []
        for path in paths:
            task.append(make_column_task(path))
        fork_join(task)
        harvest()
    
# ============================================================
# CACTUS FARM
# ============================================================

def make_pumpkin_task(path):
    def task():
        for x, y in path:
            return main.pumpkin_plant(path)
    return task

def make_replant_task(path):
    def task():
        main.replant_pumpkin(path)
    return task

def pumpkingMegafarm():
    paths = create_column_path()

    tasks = []
    for path in paths:
        tasks.append(make_pumpkin_task(path))
    all_pumpkins = fork_join(tasks)
    tasks = []
    for pumpkins in all_pumpkins:
        tasks.append(make_replant_task(pumpkins))
    fork_join(tasks)
    harvest()


def create_flower_list():
    flowers = []

    for i in range(16):
        flowers.append([])

    return flowers

def make_plant_task(path):
    def task():
        flowers = sunflower.sunflower_plantMeasure(path)

        return flowers
    return task



def make_harvest_task(flowers, petals):
    def task():
        sunflower.sunflower_harvest(flowers, petals)

    return task

def sunflowerMegaFarm():
    paths = create_column_path()
    # plant state
    plant_tasks = []
    for path in paths:
        plant_tasks.append(make_plant_task(path))

    all_flowers = fork_join(plant_tasks)

    for petals in range(15, 6, -1):
        tasks = []
        for flowers in all_flowers:
            tasks.append(make_harvest_task(flowers, petals))

        fork_join(tasks)


def water_megafarm():
    paths = create_column_path()
    def make_water_task(path):
        def task():
            for x, y in path:
                generatepath.goto_pos(x,y)
                if get_water() < 0.6:
                    use_item(Items.Water)
        return task
    water_task = []
    for path in paths:
        water_task.append(make_water_task(path))

    fork_join(water_task)


def poly_task(requests, path):
    def task():
        while True:
            for x, y in path:
                generatepath.goto_pos(x, y)
                harvestlib.polyCulture(requests)

    return task


def polyMegaFarm():
    paths = create_column_path()

    requests = {}

    # Spawn workers 1-7
    for i in range(1, len(paths)):
        task = poly_task(
            requests,
            paths[i]
        )

        spawn_drone(task)

    # Main drone permanently handles path 0
    main_task = poly_task(
        requests,
        paths[0]
    )

    main_task()

if __name__ == "__main__":
    clear()
    while True:
        polyMegaFarm()
        # pumpkingMegafarm()
        # cactus_farm()
        # sunflowerMegaFarm()
