from typing import Optional
import sys
from pathlib import Path

ROOT_DIR_PATH = str(Path(__file__).resolve().parents[2])
if ROOT_DIR_PATH not in sys.path:
    sys.path.insert(0, ROOT_DIR_PATH)

from lib.game_entities.building import (Building, BuildingHeadQuarters, BuildingSolarPanels, BuildingDrillingStation,
    BuildingWarehouse, BuildingLiquidTank, BuildingElectrolysisStation, BuildingFurnace, BuildingSpaceport,
    BuildingGreenhouse, BuildingSchool, BuildingFactory)


class Colony:

    building_types_dict: dict[str, type] = {
        "headquarters": BuildingHeadQuarters,
        "solar_panels": BuildingSolarPanels,
        "warehouse": BuildingWarehouse,
        "liquid_tank": BuildingLiquidTank,
        "drilling_station": BuildingDrillingStation,
        "furnace": BuildingFurnace,
        "electrolysis_station": BuildingElectrolysisStation,
        "greenhouse": BuildingGreenhouse,
        "school": BuildingSchool,
        "factory": BuildingFactory,
        "spaceport": BuildingSpaceport
    }

    def __init__(self, production_factors = {}, starting_colony: bool = False):
        # buildings (matrix of Building objects, 7x7)
        self.building_grid: list[list[Optional[Building]]] = [[None for column_index in range(7)] for line_index in range(7)]
        # self.selected_building_tile_coords = (x, y) = (column index, line index)
        self.selected_building_tile_coords: Optional[tuple[int, int]] = None
        # colony data
        self.data = {}
        # resources
        self.data["resources"] = {
            # "power": 0,
            "food": 0,
            "water": 0,
            "oxygen": 0,
            "hydrogen": 0,
            "iron_ore": 0,
            "iron": 0,
            "aluminium_ore": 0,
            "aluminium": 0,
            "copper_ore": 0,
            "copper": 0,
            "titanium_ore": 0,
            "titanium": 0
        }
        # resource buffer for the buildings production
        self.data["resources_buffer"] = {
            "food": 0,
            "water": 0,
            "oxygen": 0,
            "hydrogen": 0,
            "iron_ore": 0,
            "iron": 0,
            "aluminium_ore": 0,
            "aluminium": 0,
            "copper_ore": 0,
            "copper": 0,
            "titanium_ore": 0,
            "titanium": 0
        }
        # production factors
        self.data["production_factors"] = {
            "water": 1.,
            "iron_ore": 1.,
            "copper_ore": 1.,
            "aluminium_ore": 1.,
            "titanium_ore": 1.
        }
        self.data["production_factors"].update(production_factors)
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
        # self.data["spaceships"] = {
        #     "spaceship_small": 0,
        #     "spaceship_medium": 0,
        #     "spaceship_large": 0
        # }
        # # spaceship modules
        # self.data["spaceship_modules"] = {
        #     "module_cargo_hold": 0,
        #     "module_liquid_tanks": 0,
        #     "module_passengers": 0,
        #     "module_headquarters": 0
        # }
        self.data["items"] = {
            "spaceship_small": 0,
            "spaceship_medium": 0,
            "spaceship_large": 0,
            "module_cargo_hold": 0,
            "module_liquid_tanks": 0,
            "module_passengers": 0,
            "module_headquarters": 0
        }
        # special init if colony is the starting colony
        self.starting_colony = starting_colony
        if self.starting_colony:
            # add starter buildings
            self.building_grid[3][3] = BuildingHeadQuarters(self.data)
            self.building_grid[0][0] = BuildingSolarPanels(self.data)
            self.building_grid[0][0].level = 1
            self.building_grid[0][0].is_constructing = False
            self.building_grid[0][1] = BuildingDrillingStation(self.data)
            self.building_grid[0][1].level = 1
            self.building_grid[0][1].is_constructing = False
            self.building_grid[0][2] = BuildingWarehouse(self.data)
            self.building_grid[0][2].level = 1
            self.building_grid[0][2].is_constructing = False
            self.building_grid[0][3] = BuildingLiquidTank(self.data)
            self.building_grid[0][3].level = 1
            self.building_grid[0][3].is_constructing = False
            self.building_grid[0][4] = BuildingElectrolysisStation(self.data)
            self.building_grid[0][4].level = 1
            self.building_grid[0][4].is_constructing = False
            self.building_grid[0][5] = BuildingFurnace(self.data)
            self.building_grid[0][5].level = 1
            self.building_grid[0][5].is_constructing = False
            self.building_grid[0][6] = BuildingSpaceport(self.data)
            self.building_grid[0][6].level = 1
            self.building_grid[0][6].is_constructing = False
            self.building_grid[1][0] = BuildingGreenhouse(self.data)
            self.building_grid[1][0].level = 1
            self.building_grid[1][0].is_constructing = False
            self.building_grid[1][1] = BuildingSchool(self.data)
            self.building_grid[1][1].level = 1
            self.building_grid[1][1].is_constructing = False
            self.building_grid[1][2] = BuildingFactory(self.data)
            self.building_grid[1][2].level = 1
            self.building_grid[1][2].is_constructing = False
            # add people
            self.data["workers"]["engineers"]["available"] = self.data["workers"]["engineers"]["total"] = 20
            self.data["workers"]["scientists"]["available"] = self.data["workers"]["scientists"]["total"] = 20

    @property
    def power(self) -> dict[str, int]:
        power = {
            "consumed": 0,
            "produced": 0
        }
        for line_index in range(7):
            for column_index in range(7):
                building = self.building_grid[line_index][column_index]
                if building is not None:
                    # if the building is in construction, it consumes the power of its next level
                    if building.is_constructing:
                        building_power_consumed = building.parameters_per_level[building.level + 1]["power"]["consumed"]
                    else:
                        building_power_consumed = building.parameters["power"]["consumed"]
                    power["consumed"] += building_power_consumed
                    power["produced"] += building.parameters["power"]["produced"]
        return power

    @property
    def max_storage(self) -> dict[str, int]:
        max_storage = {
            "food": 0,
            "water": 0,
            "oxygen": 0,
            "hydrogen": 0,
            "iron_ore": 0,
            "iron": 0,
            "aluminium_ore": 0,
            "aluminium": 0,
            "copper_ore": 0,
            "copper": 0,
            "titanium_ore": 0,
            "titanium": 0
        }
        for line_index in range(7):
            for column_index in range(7):
                building = self.building_grid[line_index][column_index]
                if building is not None:
                    building_storage = building.parameters["storage"]
                    if building_storage is not None:
                        for resource in building_storage.keys():
                            max_storage[resource] += building_storage[resource]
        return max_storage

    @property
    def selected_building(self) -> Optional[Building]:
        return self.building_grid[self.selected_building_tile_coords[1]][self.selected_building_tile_coords[0]]

    @selected_building.setter
    def selected_building(self, building: Optional[Building]):
        self.building_grid[self.selected_building_tile_coords[1]][self.selected_building_tile_coords[0]] = building


    def can_add_building(self, building_name: str) -> bool:
        # checks whether the colony has enough resources and power to add the building
        can_add_building = True
        # check available power
        power = self.power
        available_power = power["produced"] - power["consumed"]
        if available_power < self.building_types_dict[building_name].parameters_per_level[1]["power"]["consumed"]:
            can_add_building = False
        # check available resources
        else:
            construction_costs = self.building_types_dict[building_name].parameters_per_level[0]["construction_costs"]
            for resource_name in construction_costs.keys():
                if self.data["resources"][resource_name] < construction_costs[resource_name]:
                    can_add_building = False
        return can_add_building


    def add_building(self, building_name: str):
        if self.can_add_building(building_name):
            # add the building to the colony
            self.selected_building = self.building_types_dict[building_name](self.data)
            # pay the resources for the building
            construction_costs = self.selected_building.parameters["construction_costs"]
            for resource_name in construction_costs.keys():
                self.data["resources"][resource_name] -= construction_costs[resource_name]


    def can_upgrade_building(self) -> bool:
        # checks whether the colony has enough resources and power to upgrade the building
        # if the building next level power requirements are not met, return False
        can_upgrade_building = True
        building = self.selected_building
        # check resources and level requirements
        if not building.can_upgrade():
            can_upgrade_building = False
        else:
            # check available power
            power = self.power
            power_available = power["produced"] - power["consumed"]
            power_required = building.parameters_per_level[building.level + 1]["power"]["consumed"] - building.parameters["power"]["consumed"]
            if power_available < power_required:
                can_upgrade_building = False
        return can_upgrade_building


    def cancel_building_construction(self):
        # cancel the selected building construction
        self.selected_building.cancel_upgrade()
        # if the building is at level 0, remove it from the building grid
        if self.selected_building.level == 0:
            self.selected_building = None
            # self.destroy_building()


    def can_destroy_building(self) -> bool:
        can_destroy_building = True
        # the selected building cannot be destroyed if the power it produces is being used
        # -> if destroying the building would make the available power negative, return False
        power = self.power
        power_available = power["produced"] - power["consumed"]
        building = self.selected_building
        if building.is_constructing:
            power_produced = building.parameters["power"]["produced"] - building.parameters_per_level[building.level + 1]["power"]["consumed"]
        else:
            power_produced = building.parameters["power"]["produced"] - building.parameters["power"]["consumed"]
        if power_available - power_produced < 0:
            can_destroy_building = False
        # it also cannot be destroyed if it is the headquarters
        return can_destroy_building and (building.name != "headquarters")


    def destroy_building(self):
        if self.can_destroy_building():
            # prepare the building for destruction
            self.selected_building.on_destruction()
            # remove the building from the building grid
            self.selected_building = None


    def land_ship(self):
        # place the landing ship and its contents inside the colony
        pass


    # def launch_ship(self):
    #     pass


    # def manufacture(self):
    #     pass


    # def train_worker(self):
    #     pass


    def update(self, dt):
        # update the resources based on the workers and the buildings
        # update manufacture time (factories, schools, furnaces)
        for line_index in range(7):
            for column_index in range(7):
                building = self.building_grid[line_index][column_index]
                if building is not None:
                    building.update(dt)
        # add the resources in the buffer to the colony, taking into account the maximum storage space of the colony
        max_storage = self.max_storage
        for resource in self.data["resources_buffer"].keys():
            if self.data["resources_buffer"][resource] > 0:
                self.data["resources"][resource] = min(max_storage[resource], self.data["resources"][resource] + self.data["resources_buffer"][resource])
                # clear the resource buffer
                self.data["resources_buffer"][resource] = 0
        # remove the resources (oxygen + food) consumed by the workers
        ...
