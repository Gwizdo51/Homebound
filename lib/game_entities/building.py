from typing import Any


class Building:
    # parent class for all types of buildings
    # defines a basic building:
    # - can assign/remove workers
    # - can enable/disable
    # - can build and upgrade

    name: str
    parameters_per_level: dict[int, Any]

    def __init__(self, colony_data: dict[str]):
        if type(self) is Building:
            raise TypeError("The Building class should not be instanciated directly")
        self.colony_data = colony_data
        # building level
        # 0: not built
        # 1, 2, 3: current building level
        self.level = 0
        self.level_max = 3
        self.assigned_workers = {
            "construction": {
                "engineers": 0,
                "scientists": 0
            },
            "production": {
                "engineers": 0,
                "scientists": 0
            }
        }
        # construction/upgrade timer
        self.is_constructing = True
        self.construction_workload_completed = 0
        # flags
        # self.enabled = True
        # self.can_disable = True

    @property
    def parameters(self) -> dict[str, Any]:
        return self.parameters_per_level[self.level]

    # @property
    # def can_construct(self):
    #     return False

    def can_upgrade(self) -> bool:
        # checks if building/upgrading is possible
        # construction is possible if every required resource is available in the colony
        if self.level == self.level_max or self.is_constructing:
            can_upgrade = False
        else:
            can_upgrade = True
            for resource_name in self.parameters["construction_costs"].keys():
                if self.colony_data["resources"][resource_name] < self.parameters["construction_costs"][resource_name]:
                    can_upgrade = False
                    break
        return can_upgrade

    def upgrade(self):
        # upgrade the building (+1 lvl)
        # only called when upgrade is possible
        self.is_constructing = True
        self.construction_workload_completed = 0
        # remove every required construction resources from the colony resources
        for resource_name in self.parameters["construction_costs"].keys():
            self.colony_data["resources"][resource_name] -= self.parameters["construction_costs"][resource_name]

    def cancel_upgrade(self):
        # cancel the current upgrade
        # remove all workers at the construction jobs
        self.assign_worker(add=False, job_type="construction", worker_type="engineers", all=True)
        # refund the resources to the colony
        for resource_name in self.parameters["construction_costs"].keys():
            self.colony_data["resources_buffer"][resource_name] += self.parameters["construction_costs"][resource_name]
        # reset the construction status
        self.is_constructing = False
        self.construction_workload_completed = 0

    def can_assign_worker(self, add: bool, job_type: str, worker_type: str) -> bool:
        assignment_possible = False
        # can only add workers if:
        # - there are vacant jobs in the building
        # - there are available workers in the colony
        if add:
            if job_type == "construction" and (not self.is_constructing):
                assignment_possible = False
            elif (self.assigned_workers[job_type][worker_type] < self.parameters["jobs"][job_type][worker_type]) and \
                (self.colony_data["workers"][worker_type]["available"] > 0):
                assignment_possible = True
        else:
            # if there are assigned workers ...
            if self.assigned_workers[job_type][worker_type] > 0:
                assignment_possible = True
        return assignment_possible

    def assign_worker(self, add: bool, job_type: str, worker_type: str, all: bool = False):
        # assign / unassign a job to a worker in this building
        # assign / unassign all of them if "all" is True
        # work_type = "construction" or "production"
        # job_type = "engineers" or "scientists"
        if self.can_assign_worker(add, job_type, worker_type):
            if add:
                if all:
                    # fill as many vacant jobs as possible
                    available_jobs = self.parameters["jobs"][job_type][worker_type] - self.assigned_workers[job_type][worker_type]
                    workers_to_assign = min(available_jobs, self.colony_data["workers"][worker_type]["available"])
                    self.colony_data["workers"][worker_type]["available"] -= workers_to_assign
                    self.assigned_workers[job_type][worker_type] += workers_to_assign
                else:
                    # assign a worker to the job
                    # remove an available worker from the colony
                    self.colony_data["workers"][worker_type]["available"] -= 1
                    # add the worker to the job
                    self.assigned_workers[job_type][worker_type] += 1
            else:
                if all:
                    # remove all workers
                    self.colony_data["workers"][worker_type]["available"] += self.assigned_workers[job_type][worker_type]
                    self.assigned_workers[job_type][worker_type] = 0
                else:
                    # add an available worker to the colony
                    self.colony_data["workers"][worker_type]["available"] += 1
                    # remove a worker from the job
                    self.assigned_workers[job_type][worker_type] -= 1

    def remove_all_workers(self):
        self.assign_worker(add=False, job_type="production", worker_type="engineers", all=True)
        self.assign_worker(add=False, job_type="production", worker_type="scientists", all=True)
        # no scientists can work in a construction job
        self.assign_worker(add=False, job_type="construction", worker_type="engineers", all=True)

    # def can_use_power_switch(self) -> bool:
    #     # whether the building can be turned on/off
    #     return False

    # def use_power_switch(self):
    #     # only used if building can be turned on/off
    #     if self.enabled:
    #         # fire every worker from the production jobs
    #         self.assign_worker(add=False, job_type="engineers", work_type="production", all=True)
    #         self.assign_worker(add=False, job_type="scientists", work_type="production", all=True)
    #     self.enabled = not self.enabled

    def on_destruction(self):
        # remove all workers
        self.remove_all_workers()
        # if the building is upgrading, cancel the upgrade
        if self.is_constructing:
            self.cancel_upgrade()

    def update(self, dt):
        # update construction status
        if self.is_constructing:
            # every assigned worker at the "construction" job makes 1 construction workload per second
            self.construction_workload_completed += self.assigned_workers["construction"]["engineers"] * dt
            # check if construction is finished
            if self.construction_workload_completed >= self.parameters["construction_workload"]:
                # stop the construction
                self.is_constructing = False
                self.construction_workload_completed = 0
                # upgrade the building
                self.level += 1
                # free every worker at the construction jobs
                # self.assign_worker(add=False, job_type="engineers", work_type="construction", all=True)
                self.assign_worker(add=False, job_type="construction", worker_type="engineers", all=True)



class BuildingHeadQuarters(Building):

    name = "headquarters"
    parameters_per_level = {
        1: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": {
                "food": 50,
                "water": 50,
                "oxygen": 50,
                "hydrogen": 50,
                "iron_ore": 250,
                "iron": 250,
                "aluminium_ore": 250,
                "aluminium": 250,
                "copper_ore": 250,
                "copper": 250,
                "titanium_ore": 250,
                "titanium": 250
            },
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        }
    }

    def __init__(self, colony_data: dict[str]):
        super().__init__(colony_data)
        # headquarters are always at level 1
        self.level = 1
        self.level_max = 1
        self.is_constructing = False
        # self.can_disable = False
        # assigned workers
        # self.assigned_jobs = {
        #     "engineers": 0,
        #     "scientists": 0
        # }
        # manufacture queue

    # @property
    # def parameters(self):
    #     return self.parameters_per_level[self.level]

    # def can_construct(self):
    #     # cannot build or upgrade the headquarters
    #     return False

    # def upgrade(self):
    #     # can't upgrade headquarters
    #     pass

    # def update(self, dt):
    #     # super().update(dt)
    #     pass


class BuildingSolarPanels(Building):

    name = "solar_panels"

    parameters_per_level = {
        0: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 5,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        1: {
            "power": {
                "consumed": 0,
                "produced": 100
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 5,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        2: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        3: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        }
    }

    # def __init__(self, colony_data):
    #     super().__init__(colony_data)
    #     self.can_disable = False

    # @property
    # def can_construct(self):
    #     # checks if building/upgrading is possible
    #     # construction is possible if every required resource is available in the colony
    #     if self.level < 3:
    #         construction_possible = True
    #         for resource in self.parameters[]
    #     else:
    #         construction_possible = False
    #     return construction_possible

    # def upgrade(self):
    #     pass

    # def update(self, dt):
    #     super().update(dt)

    # def can_use_power_switch(self):
    #     # can only be turned off if the power it produces isn't used in the colony -> check at the colony level
    #     return True


class BuildingDrillingStation(Building):

    name = "drilling_station"
    parameters_per_level = {
        0: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        1: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 5,
                    "scientists": 0
                }
            },
            "production_speed": 1
        },
        2: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1
        },
        3: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1
        }
    }

    def __init__(self, colony_data):
        super().__init__(colony_data)
        # self.resource_produced = "water", "iron_ore", "aluminium_ore", "copper_ore" or "titanium_ore"
        self.resource_produced = None

    def produce(self, resource_type: str):
        self.resource_produced = resource_type

    def update(self, dt):
        super().update(dt)
        # dump the produced resources into the colony resource buffer
        # only produce if at least level 1 and a resource to produce has been selected
        if (self.level > 0) and (self.resource_produced is not None):
            self.colony_data["resources_buffer"][self.resource_produced] += dt \
                * (self.assigned_workers["production"]["engineers"] + self.assigned_workers["production"]["scientists"]) \
                * self.parameters["production_speed"] * self.colony_data["production_factors"][self.resource_produced]


class BuildingWarehouse(Building):

    name = "warehouse"
    parameters_per_level = {
        0: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        1: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": {
                "food": 0,
                "iron_ore": 0,
                "iron": 0,
                "aluminium_ore": 0,
                "aluminium": 0,
                "copper_ore": 0,
                "copper": 0,
                "titanium_ore": 0,
                "titanium": 0
            },
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        2: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": {
                "food": 0,
                "iron_ore": 0,
                "iron": 0,
                "aluminium_ore": 0,
                "aluminium": 0,
                "copper_ore": 0,
                "copper": 0,
                "titanium_ore": 0,
                "titanium": 0
            },
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        3: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": {
                "food": 0,
                "iron_ore": 0,
                "iron": 0,
                "aluminium_ore": 0,
                "aluminium": 0,
                "copper_ore": 0,
                "copper": 0,
                "titanium_ore": 0,
                "titanium": 0
            },
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        }
    }

    # def __init__(self, colony_data):
    #     super().__init__(colony_data)
    #     self.can_disable = False


class BuildingLiquidTank(Building):

    name = "liquid_tank"
    parameters_per_level = {
        0: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        1: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": {
                "water": 0,
                "oxygen": 0,
                "hydrogen": 0
            },
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        2: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": {
                "water": 0,
                "oxygen": 0,
                "hydrogen": 0
            },
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        3: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": {
                "water": 0,
                "oxygen": 0,
                "hydrogen": 0
            },
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        }
    }

    # def __init__(self, colony_data):
    #     super().__init__(colony_data)
    #     self.can_disable = False


class BuildingElectrolysisStation(Building):

    name = "electrolysis_station"
    parameters_per_level = {
        0: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        1: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1
        },
        2: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1
        },
        3: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1
        }
    }

    def update(self, dt):
        super().update(dt)
        # dump the produced resources into the colony resource buffer
        # only produce if at least level 1
        if self.level > 0:
            # consume water
            water_required_from_storage = dt * self.parameters["production_speed"] \
                * (self.assigned_workers["production"]["engineers"] + self.assigned_workers["production"]["scientists"])
            water_obtained = min(water_required_from_storage, self.colony_data["resources"]["water"])
            self.colony_data["resources"]["water"] -= water_obtained
            # produce oxygen
            self.colony_data["resources_buffer"]["oxygen"] += water_obtained * (1/2)
            # produce hydrogen
            self.colony_data["resources_buffer"]["hydrogen"] += water_obtained * 1


class BuildingFurnace(Building):

    name = "furnace"
    parameters_per_level = {
        0: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        1: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1,
            "production_per_cycle": 1
        },
        2: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1,
            "production_per_cycle": 1
        },
        3: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1,
            "production_per_cycle": 1
        }
    }

    # ore to ingot ratio : 2/1

    def __init__(self, colony_data):
        super().__init__(colony_data)
        # self.resource_produced = "iron", "aluminium", "copper" or "titanium"
        self.resource_produced = None
        self.smelting_completed_percent = 0
        # whether ore has been consumed for the current cycle
        self.ore_consumed = False

    def switch_production(self, resource_type: str):
        if self.resource_produced != resource_type:
            # reset the smelting cycle
            self.smelting_completed_percent = 0
            self.ore_consumed = False
        self.resource_produced = resource_type

    # def use_power_switch(self):
    #     # reset the smelting cycle if the building is turned off
    #     if self.enabled:
    #         self.smelting_completed_percent = 0
    #         self.ore_consumed = False
    #     super().use_power_switch()

    def _try_start_cycle(self):
        ore_to_consume = self.resource_produced + "_ore"
        # if the colony has enough ore to start a cycle ...
        if self.colony_data["resources"][ore_to_consume] >= 2 * self.parameters["production_per_cycle"]:
            # consume the ore
            self.colony_data["resources"][ore_to_consume] -= 2 * self.parameters["production_per_cycle"]
            self.ore_consumed = True

    def update(self, dt):
        super().update(dt)
        # dump the produced resources into the colony resource buffer
        # only produce if at least level 1 and a resource to produce has been selected
        if (self.level > 0) and (self.resource_produced is not None):
            if not self.ore_consumed:
                # try to consume ore for the next production cycle
                self._try_start_cycle()
            if self.ore_consumed:
                self.smelting_completed_percent += dt * self.parameters["production_speed"] \
                    * (self.assigned_workers["production"]["engineers"] + self.assigned_workers["production"]["scientists"])
                # if the cycle is completed ...
                if self.smelting_completed_percent >= 100:
                    # add the resource to the buffer
                    self.colony_data["resources_buffer"][self.resource_produced] += self.parameters["production_per_cycle"]
                    # reset the cycle
                    self.smelting_completed_percent = 0
                    self.ore_consumed = False


class BuildingSpaceport(Building):

    name = "spaceport"
    parameters_per_level = {
        0: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        1: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        }
    }

    def __init__(self, colony_data):
        super().__init__(colony_data)
        self.level_max = 1


class BuildingGreenhouse(Building):

    name = "greenhouse"
    parameters_per_level = {
        0: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        1: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1
        },
        2: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1
        },
        3: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1
        }
    }

    def update(self, dt):
        super().update(dt)
        # dump the produced resources into the colony resource buffer
        # only produce if at least level 1
        if self.level > 0:
            # consume water
            water_required_from_storage = dt * self.parameters["production_speed"] \
                * (self.assigned_workers["production"]["engineers"] + self.assigned_workers["production"]["scientists"])
            water_obtained = min(water_required_from_storage, self.colony_data["resources"]["water"])
            self.colony_data["resources"]["water"] -= water_obtained
            # produce food
            self.colony_data["resources_buffer"]["food"] += water_obtained * 5
            # produce oxygen
            self.colony_data["resources_buffer"]["oxygen"] += water_obtained * 1


class BuildingSchool(Building):

    name = "school"
    items_workload = {
        "engineers": 0,
        "scientists": 0,
        "pilots": 0
    }

    parameters_per_level = {
        0: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        1: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 5
                }
            },
            "production_speed": 1,
            "queue_max_size": 5
        },
        2: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1,
            "queue_max_size": 5
        },
        3: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1,
            "queue_max_size": 5
        }
    }

    def __init__(self, colony_data):
        super().__init__(colony_data)
        self.training_queue = []
        self.training_workload_completed = 0

    def can_add_worker(self) -> bool:
        return len(self.training_queue) < self.parameters["queue_max_size"]

    def add_worker_to_queue(self, worker_type):
        # worker_type = "engineers", "scientists" or "pilots"
        # add a worker to the queue only if it isn't full
        if self.can_add_worker():
            self.training_queue.append(worker_type)

    def can_cancel_training(self) -> bool:
        return len(self.training_queue) > 0

    def cancel_training(self):
        # can be called even if impossible (update != on_draw)
        if self.can_cancel_training():
            # cancel the current training worker
            self.training_queue.pop(0)
            self.training_workload_completed = 0

    def can_clear_queue(self) -> bool:
        return len(self.training_queue) > 1

    def clear_queue(self):
        # can be called even if impossible (update != on_draw)
        if self.can_clear_queue():
            # clear the queue (everything but the current training worker)
            self.training_queue = [self.training_queue[0]]

    # def use_power_switch(self):
    #     # clear the queue and reset the training cycle if the building is turned off
    #     if self.enabled:
    #         # self.training_queue = []
    #         # self.training_workload_completed = 0
    #         while self.can_cancel_training():
    #             self.can_cancel_training()
    #     super().use_power_switch()

    def update(self, dt):
        super().update(dt)
        # only train if at least level 1 and the training queue is not empty
        if (self.level > 0) and (len(self.training_queue) > 0):
            self.training_workload_completed += dt * self.parameters["production_speed"] \
                * (self.assigned_workers["production"]["engineers"] + self.assigned_workers["production"]["scientists"])
            # if the cycle is completed ...
            if self.training_workload_completed >= self.items_workload[self.training_queue[0]]:
                # add the worker to the colony
                self.colony_data["workers"][self.training_queue[0]]["available"] += 1
                self.colony_data["workers"][self.training_queue[0]]["total"] += 1
                # remove the first element from the queue and reset the cycle
                self.training_queue.pop(0)
                self.training_workload_completed = 0


class BuildingFactory(Building):

    name = "factory"
    items_price = {
        "spaceship_small": {
            "resources": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "workload": 0
        },
        "spaceship_medium": {
            "resources": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "workload": 0
        },
        "spaceship_large": {
            "resources": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "workload": 0
        },
        "module_cargo_hold": {
            "resources": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "workload": 0
        },
        "module_liquid_tanks": {
            "resources": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "workload": 0
        },
        "module_passengers": {
            "resources": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "workload": 0
        },
        "module_headquarters": {
            "resources": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "workload": 0
        },
    }

    parameters_per_level = {
        0: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            }
        },
        1: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1,
            "queue_max_size": 5
        },
        2: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "construction_costs": {
                "iron": 0,
                "aluminium": 0,
                "copper": 0,
                "titanium": 0
            },
            "construction_workload": 100,
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1,
            "queue_max_size": 5
        },
        3: {
            "power": {
                "consumed": 0,
                "produced": 0
            },
            "storage": None,
            "jobs": {
                "construction": {
                    "engineers": 0,
                    "scientists": 0
                },
                "production": {
                    "engineers": 0,
                    "scientists": 0
                }
            },
            "production_speed": 1,
            "queue_max_size": 5
        }
    }

    def __init__(self, colony_data):
        super().__init__(colony_data)
        self.items_queue = []
        self.item_workload_completed = 0

    def can_make_item(self, item_name: str) -> bool:
        # check if the queue is full
        if len(self.items_queue) >= self.parameters["queue_max_size"]:
            can_make_item = False
        else:
            # check if the colony has enough resources to make the item
            can_make_item = True
            item_resources_required = self.items_price[item_name]["resources"]
            for resource_name in item_resources_required.keys():
                if self.colony_data["resources"][resource_name] < item_resources_required[resource_name]:
                    can_make_item = False
                    break
        return can_make_item

    def add_item_to_queue(self, item_name: str):
        if self.can_make_item(item_name):
            # pay the item price
            item_resources_required = self.items_price[item_name]["resources"]
            for resource_name in item_resources_required.keys():
                self.colony_data["resources"][resource_name] -= item_resources_required[resource_name]
            # add the item to the list
            self.items_queue.append(item_name)

    def can_cancel_item(self) -> bool:
        return len(self.items_queue) > 0

    def cancel_item(self):
        # can be called even if impossible (update != on_draw)
        if self.can_cancel_item():
            # give the resources back to the colony
            item_resources_required = self.items_price[self.items_queue[0]]["resources"]
            for resource_name in item_resources_required.keys():
                self.colony_data["resources_buffer"][resource_name] += item_resources_required[resource_name]
            # cancel the current item
            self.items_queue.pop(0)
            self.item_workload_completed = 0

    def can_clear_queue(self) -> bool:
        return len(self.items_queue) > 1

    def clear_queue(self):
        # can be called even if impossible (update != on_draw)
        # while the queue contains more than 1 item ...
        while len(self.items_queue) > 1:
            # delete the last item of the queue
            item_deleted = self.items_queue.pop(-1)
            # give the resources of the item deleted back to the colony
            item_resources_required = self.items_price[item_deleted]["resources"]
            for resource_name in item_resources_required.keys():
                self.colony_data["resources_buffer"][resource_name] += item_resources_required[resource_name]

    # def use_power_switch(self):
    #     # clear the queue and reset the workload completed if the building is turned off
    #     if self.enabled:
    #         # self.items_queue = []
    #         # self.item_workload_completed = 0
    #         while self.can_cancel_item():
    #             self.cancel_item()
    #     super().use_power_switch()

    def on_destruction(self):
        super().on_destruction()
        # cancel every queued item
        while self.can_cancel_item():
            self.cancel_item()

    def update(self, dt):
        super().update(dt)
        # only make item if at least level 1 and the training queue is not empty
        if (self.level > 0) and (len(self.items_queue) > 0):
            self.item_workload_completed += dt * self.parameters["production_speed"] \
                * (self.assigned_workers["production"]["engineers"] + self.assigned_workers["production"]["scientists"])
            # if the cycle is completed ...
            if self.item_workload_completed >= self.items_price[self.items_queue[0]]["workload"]:
                # add the item to the colony
                self.colony_data["items"][self.items_queue[0]] += 1
                # remove the first element from the queue and reset the cycle
                self.items_queue.pop(0)
                self.item_workload_completed = 0


class BuildingResearchLabs(Building):

    # forget for now
    def __init__(self, colony_data):
        raise NotImplementedError("research labs not yet implemented")
