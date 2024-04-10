import sys
from pathlib import Path

ROOT_DIR_PATH = str(Path(__file__).resolve().parents[2])
if ROOT_DIR_PATH not in sys.path:
    sys.path.insert(0, ROOT_DIR_PATH)

from lib.game_entities.building import Building, BuildingHeadQuarters, BuildingSolarPanels


class Colony:

    def __init__(self, production_factors = {}, starting_colony: bool = False):
        # buildings (matrix of Building objects, 7x7)
        self.building_grid = [[None for i in range(7)] for j in range(7)]
        # colony data
        self.data = {}
        # resources
        self.data["resources"] = {
            # "power": 0,
            "food": 0,
            "water": 0,
            "oxygen": 0,
            "hydrogen": 0,
            "iron ore": 0,
            "iron": 0,
            "aluminium ore": 0,
            "aluminium": 0,
            "copper ore": 0,
            "copper": 0,
            "titanium ore": 0,
            "titanium": 0
        }
        # production factors
        self.data["production_factors"] = {
            "water": 1.,
            "iron ore": 1.,
            "copper ore": 1.,
            "aluminium ore": 1.,
            "titanium ore": 1.
        }
        # workers
        self.data["workers"] = {
            "engineers": {
                "available": 0,
                "total": 0
            },
            "scientists": {
                "available": 0,
                "total": 0
            },
            "pilots": 0
        }
        # landed spaceships
        self.data["spaceships"] = {
            "class_0": 0,
            "class_1": 0,
            "class_2": 0
        }
        # spaceship modules
        self.data["spaceship_modules"] = {}
        # special init if colony is the starting colony
        self.starting_colony = starting_colony
        if self.starting_colony:
            ...

    @property
    def power(self) -> dict[str, int]:
        return {
            "consumed": 0,
            "produced": 0
        }

    @property
    def max_storage(self) -> dict[str, int]:
        return {
            "food": 0,
            "water": 0,
            "oxygen": 0,
            "hydrogen": 0,
            "iron ore": 0,
            "iron": 0,
            "aluminium ore": 0,
            "aluminium": 0,
            "copper ore": 0,
            "copper": 0,
            "titanium ore": 0,
            "titanium": 0
        }


    def can_add_building(self, type) -> bool:
        # checks whether the colony has enough resources and power to add the building
        return True


    def can_upgrade_building(self) -> bool:
        # checks whether the colony has enough resources and power to upgrade the building
        return True


    def add_building(self, type, index_line, index_column):
        pass


    def cancel_building(self, type, index_line, index_column):
        pass


    def can_disable_building(self) -> bool:
        # checks whether the building can be turned off
        # if the building is a solar panel, prevent turning it off if the power it produces is used
        pass


    def destroy_building(self):
        pass


    def land_ship(self):
        # place the landing ship and its contents inside the colony
        pass


    # def launch_ship(self):
    #     pass


    def manufacture(self):
        pass


    def train_worker(self):
        pass


    def update(self, dt):
        # update the resources based on the workers and the buildings
        # update manufacture time (factories, schools)
        for line_index in range(7):
            for column_index in range(7):
                building = self.building_grid[line_index][column_index]
                if building is not None:
                    building.update(dt)
