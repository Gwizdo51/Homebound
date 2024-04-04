class Colony:

    def __init__(self, production_factors = {}, starting_colony: bool = False):
        # buildings (matrix of Building objects, 7x7)
        self.building_grid = [[None for i in range(7)] for j in range(7)]
        # landed spaceships
        self.spaceships = {
            "class_0": 0,
            "class_1": 0,
            "class_2": 0
        }
        # resources
        self.resources = {
            "power": 0,
            "food": 0,
            "water": 0,
            "oxygen": 0,
            "hydrogen": 0,
            "iron ore": 0,
            "iron": 0,
            "copper ore": 0,
            "copper": 0,
            "uranium ore": 0,
            "uranium": 0
        }
        # production factors
        self.production_factors = {
            "water": 1.,
            "iron ore": 1.,
            "copper ore": 1.,
            "uranium ore": 1.
        }
        # workers
        self.workers = {
            "engineer": 0,
            "scientist": 0,
            "pilot": 0
        }
        # special init if colony is the starting colony
        self.starting_colony = starting_colony
        if starting_colony:
            ...


    def add_building(self):
        pass


    def delete_building(self):
        pass


    def land_ship(self):
        # place the landing ship and its contents inside the colony
        pass


    def launch_ship(self):
        pass


    def manufacture(self):
        pass


    def train_worker(self):
        pass


    def update(self, dt):
        # update the resources based on the workers and the buildings
        # update manufacture time (factories, schools)
        pass
